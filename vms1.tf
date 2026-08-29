data "yandex_compute_image" "ubuntu_2204_lts" {
  family = "ubuntu-2204-lts"
}

locals {
  vm_count   = 2
  ssh_user   = "user"
  ssh_key_path = "/home/ivanovfn/.ssh/id_ed25519"
}

resource "yandex_vpc_network" "network1" {
  name = "network1"
}

resource "yandex_vpc_gateway" "nat_gateway" {
  name = "fops-gateway-${var.flow}"
  shared_egress_gateway {}
}

resource "yandex_vpc_route_table" "rt" {
  name       = "fops-route-table-${var.flow}"
  network_id = yandex_vpc_network.network1.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    gateway_id         = yandex_vpc_gateway.nat_gateway.id
  }
}

resource "yandex_vpc_subnet" "subnet1" {
  name          = "subnet1"
  network_id    = yandex_vpc_network.network1.id
  v4_cidr_blocks = ["172.24.8.0/24"]
  zone          = "ru-central1-a"
  route_table_id = yandex_vpc_route_table.rt.id
}

resource "yandex_compute_instance" "vm" {
  count = local.vm_count

  name        = "vm${count.index}"
  hostname    = "vm${count.index}"
  platform_id = "standard-v1"
  zone        = "ru-central1-a"

  resources {
    cores         = 2
    memory        = 2
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id   = data.yandex_compute_image.ubuntu_2204_lts.image_id
      type       = "network-hdd"
      size       = 10
    }
  }

  metadata = {
    user-data          = file("./cloud-init.yml")
    serial-port-enable = 1
  }

  scheduling_policy {
    preemptible = false
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet1.id
    nat       = true
  }
}

resource "yandex_lb_target_group" "group1" {
  name = "group1"

  target {
    subnet_id = yandex_vpc_subnet.subnet1.id
    address   = yandex_compute_instance.vm[0].network_interface[0].ip_address
  }

  target {
    subnet_id = yandex_vpc_subnet.subnet1.id
    address   = yandex_compute_instance.vm[1].network_interface[0].ip_address
  }
}

resource "yandex_lb_network_load_balancer" "balancer1" {
  name                = "balancer1"
  deletion_protection = false

  listener {
    name = "my-lb1"
    port = 80

    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.group1.id

    healthcheck {
      name = "http"

      http_options {
        port  = 80
        path  = "/"
      }

      interval             = 10
      timeout              = 5
      unhealthy_threshold  = 2
      healthy_threshold    = 2
    }
  }
}

resource "local_file" "inventory" {
  content = <<EOF
[webservers]
${yandex_compute_instance.vm[0].network_interface[0].nat_ip_address}
${yandex_compute_instance.vm[1].network_interface[0].nat_ip_address}

[all:vars]
ansible_user=${local.ssh_user}
ansible_ssh_private_key_file=${local.ssh_key_path}
EOF
  filename = "./hosts.ini"
  depends_on = [yandex_compute_instance.vm]
}