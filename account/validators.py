import re
from django.core.exceptions import ValidationError

class CapitalLetterValidator:
    def validate(self,password,user=None):
        if not any(char.isupper() for char in password):            
            raise ValidationError(
                'Password must contain at least one capital letter.',
                code='password_must_contain_capital_letter',
                )
                
