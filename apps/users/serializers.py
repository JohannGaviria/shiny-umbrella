from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación y creación de usuarios.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (USer): Modelo de usuario.
            fields (list): Campos del serializador.
        """
        model = User
        fields = ['id', 'username', 'email', 'password']
    

    def validate_email(self, value):
        """
        Valida que el correo electrónico sea único.

        Args:
            value (str): Correo electrónico a validar.

        Returns:
            str: Correo electrónico validado.

        Raises:
            serializers.ValidationError: Si el correo electrónico ya está en uso.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"This email {value} is already in use.")
        return value
    

    def validate_password(self, value):
        """
        Valida que la contraseña sea segura.

        Args:
            value (str): Contraseña a validar.

        Returns:
            str: Contraseña validada.

        Raises:
            serializers.ValidationError: Si la contraseña no cumple con los requisitos de seguridad.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)    
        return value
    
    
    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.

        Args:
            validated_data (dict): Datos validados para crear el usuario.

        Returns:
            User: Usuario creado.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de datos de usuario.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (User): Modelo de usuario.
            fields (list): Campos del serializador.
        """
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para la actualización de datos de usuario.
    """
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (User): Modelo de usuario.
            fields (list): Campos del serializador.
        """
        model = User
        fields = ['id', 'username', 'email', 'current_password', 'new_password']


    def validate_email(self, value):
        """
        Valida que el correo electrónico sea único.

        Args:
            value (str): Correo electrónico a validar.

        Returns:
            str: Correo electrónico validado.

        Raises:
            serializers.ValidationError: Si el correo electrónico ya está en uso.
        """
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(f"This email {value} is already in use.")
        return value
    

    def validate(self, attrs):
        """
        Valida los atributos proporcionados para cambiar la contraseña de un usuario.

        Args:
            attrs (dict): Atributos a validar.

        Returns:
            dict: Atributos validados.

        Raises:
            serializers.ValidationError: Si alguna validación falla.
        """
        self.validate_current_password_provided(attrs)
        self.validate_current_password_correct(attrs)
        self.validate_new_password(attrs)

        return attrs


    def validate_current_password_provided(self, attrs):
        """
        Valida que se proporcione la contraseña actual si se quiere cambiar la nueva contraseña.

        Args:
            attrs (dict): Atributos a validar.

        Raises:
            serializers.ValidationError: Si no se proporciona la contraseña actual.
        """
        if 'new_password' in attrs and not attrs.get('current_password'):
            raise serializers.ValidationError({
                'current_password': 'Current password is required to set a new password.'
            })


    def validate_current_password_correct(self, attrs):
        """
        Verifica la contraseña actual si se está cambiando la nueva contraseña.

        Args:
            attrs (dict): Atributos a validar.

        Raises:
            serializers.ValidationError: Si la contraseña actual es incorrecta.
        """
        if 'current_password' in attrs and 'new_password' in attrs:
            user = self.instance
            if not user.check_password(attrs['current_password']):
                raise serializers.ValidationError({
                    'current_password': 'Current password is incorrect.'
                })


    def validate_new_password(self, attrs):
        """
        Valida la nueva contraseña.

        Args:
            attrs (dict): Atributos a validar.

        Raises:
            serializers.ValidationError: Si la nueva contraseña no cumple con los requisitos de seguridad.
        """
        if 'new_password' in attrs:
            user = self.instance
            try:
                validate_password(attrs['new_password'], user)
            except ValidationError as e:
                raise serializers.ValidationError({
                    'new_password': e.messages
                })
        return attrs


    def update(self, instance, validated_data):
        """
        Actualiza los datos del usuario.

        Args:
            instance (User): Instancia del usuario a actualizar.
            validated_data (dict): Datos validados para actualizar el usuario.

        Returns:
            User: Usuario actualizado.
        """
        # Actualiza los campos del usuario
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Actualiza la contraseña si se proporciona
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])

        # Guarda los cambios
        instance.save()
        return instance
