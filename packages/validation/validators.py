"""Validators for finance documents."""

import re
from typing import Any


class ImeiValidator:
    """IMEI validation using Luhn algorithm."""

    @staticmethod
    def validate(imei: str) -> bool:
        """Validate IMEI number.
        
        Args:
            imei: IMEI number to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Remove any non-digit characters
        imei = re.sub(r"\D", "", imei)

        # IMEI should be 15 digits
        if len(imei) != 15:
            return False

        # Apply Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(imei)):
            n = int(digit)
            if i % 2 == 1:  # Every second digit from right
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return total % 10 == 0


class PhoneValidator:
    """Phone number validation."""

    @staticmethod
    def validate(phone: str, country_code: str = "US") -> bool:
        """Validate phone number.
        
        Args:
            phone: Phone number to validate
            country_code: Country code (default: US)
            
        Returns:
            True if valid, False otherwise
        """
        # Remove common separators
        phone = re.sub(r"[\s\-\(\)\+]", "", phone)

        # Basic validation: 10-15 digits
        if not re.match(r"^\d{10,15}$", phone):
            return False

        return True


class CurrencyValidator:
    """Currency validation."""

    VALID_CURRENCIES = {
        "USD", "EUR", "GBP", "INR", "JPY", "AUD",
        "CAD", "CHF", "CNY", "SEK", "NZD", "MXN",
        "SGD", "HKD", "NOK", "KRW", "TRY", "RUB",
        "BRL", "ZAR", "AED", "SAR", "QAR"
    }

    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate currency code.
        
        Args:
            code: Currency code
            
        Returns:
            True if valid, False otherwise
        """
        return code.upper() in CurrencyValidator.VALID_CURRENCIES

    @staticmethod
    def validate_amount(amount: Any) -> bool:
        """Validate currency amount.
        
        Args:
            amount: Amount to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            num = float(amount)
            return num >= 0
        except (ValueError, TypeError):
            return False
