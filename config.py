# config.py
import os
import time
from threading import RLock
from functools import lru_cache

# Only load .env when NOT running in Azure App Service.
# App Service sets WEBSITE_SITE_NAME automatically.
if os.getenv("WEBSITE_SITE_NAME") is None:
    from dotenv import load_dotenv
    load_dotenv()

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = os.getenv("KEY_VAULT_URL")  # e.g., https://myvault.vault.azure.net/

@lru_cache
def _credential():
    # DefaultAzureCredential will use Managed Identity on App Service.
    # exclude_interactive_browser_credential=True prevents a browser pop-up locally.
    return DefaultAzureCredential(exclude_interactive_browser_credential=True)

@lru_cache
def _kv_client():
    if not VAULT_URL:
        return None
    # IMPORTANT: use named parameters
    return SecretClient(vault_url=VAULT_URL, credential=_credential())

class SecretCache:
    """Simple in-memory TTL cache to avoid hitting Key Vault on every request."""
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._cache = {}
        self._lock = RLock()

    def get(self, name: str, loader):
        now = time.time()
        with self._lock:
            entry = self._cache.get(name)
            if entry and now - entry["ts"] < self.ttl:
                return entry["value"]
            value = loader(name)
            self._cache[name] = {"value": value, "ts": now}
            return value

_secret_cache = SecretCache(ttl_seconds=int(os.getenv("KV_SECRET_TTL", "300")))

class Config:
    """
    get_secret("MY_SECRET") will:
      - If KEY_VAULT_URL is set and MSI/RBAC allows it → read from Key Vault “my-secret”
      - Else → fall back to environment variable MY_SECRET
    """
    @staticmethod
    def get_secret(secret_name: str) -> str | None:
        # Your convention: env uses underscores, KV uses hyphens
        kv_secret_name = secret_name.replace("_", "-")

        # If no vault configured, fall back to env
        if not VAULT_URL:
            return os.getenv(secret_name)

        client = _kv_client()
        if client is None:
            return os.getenv(secret_name)

        def _load_from_kv(name: str):
            try:
                return client.get_secret(name).value
            except Exception:
                # Any 403/404/network issue → fall back to env
                return os.getenv(secret_name)

        return _secret_cache.get(kv_secret_name, _load_from_kv)


