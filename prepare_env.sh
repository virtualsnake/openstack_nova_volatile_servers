#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cat << EOF > ${SCRIPT_DIR}/openstack.env
export OS_AUTH_URL="${OS_AUTH_URL}"
export OS_IDENTITY_API_VERSION="${OS_IDENTITY_API_VERSION}"
export OS_VOLUME_API_VERSION="${OS_VOLUME_API_VERSION}"
export CLIFF_FIT_WIDTH="${CLIFF_FIT_WIDTH}"
export OS_PROJECT_DOMAIN_NAME="${OS_PROJECT_DOMAIN_NAME}"
export OS_PROJECT_ID="${OS_PROJECT_ID}"
export OS_TENANT_ID="${OS_TENANT_ID}"
export OS_REGION_NAME="${OS_REGION_NAME}"
export OS_USER_DOMAIN_NAME="${OS_USER_DOMAIN_NAME}"
export OS_USERNAME="${OS_USERNAME}"
export OS_PASSWORD="\$(echo "$(echo "${OS_PASSWORD}" | base64)" | base64 -d)"
EOF