class WalletAddressConverter:
    regex = "^0x[a-fA-F0-9]{40}$"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value