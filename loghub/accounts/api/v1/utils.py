from accounts.models import Professional


def add_professionals(user, professionals_data, professional_ids):

    for professional_data in professionals_data:
        professional, created = Professional.objects.get_or_create(**professional_data)
        user.professional.add(professional)

    for professional_id in professional_ids:
        try:
            professional = Professional.objects.get(id=professional_id)
            user.professional.add(professional)
        except Professional.DoesNotExist:
            pass