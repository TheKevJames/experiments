# In Terraform, we could configure the relevant policies with the following
# bindings for any new APIs we deploy. You could, of course, configure the
# following manually in the GCP UI, but describing this as
# infrastructure-as-code has a bunch of advantages; most relevant in this case
# is that the addition of new routes as you add features becomes much more
# straightforward than needing to manually duplicate past configuration.
#
# Note that Google does not allow KMS resources to be deleted, so all the
# following resources should have `lifecycle {prevent_destroy = true}` to
# ensure Terraform state always matches Google's. Omitted for brevity.
#
# Similarly, all these resources should be created within
# `project = "my-gcp-project"`. Each GCP project would have the same resources
# defined. Omitted for brevity.

# In order to be deliberate in our authentication, the best practice is to
# ensure each unique resource has its own service account. This allows us to be
# as selective as we need to be in terms of setting access policies and gives
# us things like per-service access logging for free.
resource "google_service_account" "api-my-api-service" {
  account_id   = "api-my-api-service"
  display_name = "API (my-api-service)"
}

# We create one keyring per API service.
resource "google_kms_key_ring" "my-api-service" {
  name     = "my-api-service"
  location = "global"
}

# Only the relevant API's service account would be marked as being able to
# descrypt requests. It would theoretically be safe to allow more resources to
# decrypt, eg. developers could be given access in order to be able to make use
# of this system locally.
resource "google_kms_key_ring_iam_binding" "key_ring" {
  key_ring_id = "${google_kms_key_ring.my-api-service.self_link}"
  role        = "roles/cloudkms.cryptoKeyDecrypter"

  members = [
    "serviceAccount:${google_service_account.api-my-api-service.email}",
    "group:developers@company.com",
  ]
}

# One key per route within that service. Note that they may each have different
# access levels, for example:
locals {
  routes_standard = ["create-resource", "view-resource", ...]
  routes_admin = ["modify-settings", ...]
  # etc.
}

resource "google_kms_crypto_key" "routes-standard" {
  count = "${len(local.routes_standard)}"

  name            = "${local.routes_standard[count.index]}"
  key_ring        = "${google_kms_key_ring.my-api-service.self_link}"
  # Daily key rotation (the minimum offered by Google KMS) allows us to be sure
  # that any user making decryptable requests was marked in the IAM bindings
  # list on that day.
  #
  # Note that rotation can be forced manually in the GCP UI or with a curl
  # request if we suspect a breach occurred -- at that point, all future KMS
  # requests would make use of the new key material.
  rotation_period = "86400s"
}

resource "google_kms_crypto_key" "routes-admin" {
  count = "${len(local.routes_admin)}"

  name            = "${local.routes_admin[count.index]}"
  key_ring        = "${google_kms_key_ring.my-api-service.self_link}"
  rotation_period = "86400s"
}

resource "google_kms_crypto_key_iam_binding" "key-standard" {
  count = "${len(local.routes_standard)}"

  crypto_key_id = "${google_kms_crypto_key.routes-standard[count.index].self_link}"
  role          = "roles/cloudkms.cryptoKeyEncrypter"

  # Any arbitrary accounts can be given access to this API by listing them
  # here.
  members = [
    "user:cto@company.com",
    "group:developers@company.com",
    "serviceaccount:some-client-app@appspot.gservice.com",
    # etc
  ]

  # Note that in some cases, you may want cascading permissions, eg. "all
  # clients with admin access also have standard access". You can use
  # Terraform primitives to solve this:
  #   members = concat([
  #     "group:standard-access-only@company.com",
  #   ], ${google_kms_crypto_key_iam_binding.key-admin[count.index].members})
}

resource "google_kms_crypto_key_iam_binding" "key-admin" {
  count = "${len(local.routes_admin)}"

  crypto_key_id = "${google_kms_crypto_key.routes-admin[count.index].self_link}"
  role          = "roles/cloudkms.cryptoKeyEncrypter"

  # Similarly, more privileged accounts could be listed here.
  members = [
    "user:cto@company.com",
    "group:admins@company.com",
    # etc
  ]
}
