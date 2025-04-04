import rsa
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.forms.widgets import Input
from django.db import models
from django.db.models import QuerySet
from django.db.models.base import ModelBase
from itertools import chain
from django.core.paginator import Paginator
from io import BytesIO
from django.core.files import File
from django.template.loader import get_template
from django.http import HttpResponse
import random
import xlwt
from datetime import datetime, date, timedelta
import qrcode
from django.conf import settings
import uuid
import hashlib
import time


class CustomDateInput(Input):
    input_type = "date"
    template_name = "django/forms/widgets/text.html"


def generate_keys():
    """Retourne les clés (publique et privée) sous forme de chaine de caractère."""
    (publicKey, privateKey) = rsa.newkeys(1024)
    privateKey = privateKey.save_pkcs1("PEM")
    publicKey = publicKey.save_pkcs1("PEM")

    return publicKey, privateKey


def load_keys(str_public, str_private):
    """Convertit les clés (publique et privée) dans leur format d'origine à partir de leur format str.

    Args:
        str_public (rsa.PublicKey): La clé publique au format str.
        str_private (rsa.PrivateKey): La clé privée au format str.

    Returns:
        privateKey, publicKey: Les clés dans leur format d'origine.
    """
    publicKey = rsa.PublicKey.load_pkcs1(str_public)
    privateKey = rsa.PrivateKey.load_pkcs1(str_private)
    return publicKey, privateKey


def encrypt(message, key):
    message_bytes = message.encode("utf-8")
    return rsa.encrypt(message_bytes, key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode("ascii")
    except Exception:
        return False


def sign_message(message, key):
    return rsa.sign(message.encode("ascii"), key, "SHA-256")


def verify_signature(message, signature, key):
    try:
        return (
            rsa.verify(
                message.encode("ascii"),
                signature,
                key,
            )
            == "SHA-256"
        )
    except Exception:
        return False


def sending_mail(mail_subject, message, sender=None, receiver=None):
    """Cette fonction permet d'envoyer des mails.

    Args:
        mail_subject (str): Le thème du mail
        message (str): Le contenu du mail
        sender (str, optional): L'adresse mail de l'emetteur.Defaults: None
        receiver (str): L'adrese mail du recepteur.
    """
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=sender,
        recipient_list=[receiver],
        fail_silently=True,
    )


def sending_beautiful_mail(template_name: str, data_to_template: dict, subject: str, sender: str, receiver: str, attachment: str = None):
    message = render_to_string(template_name, data_to_template)

    email = EmailMessage(subject, message, sender, [receiver])
    email.fail_silently = True
    email.content_subtype = "html"
    email.send()


def get_active_school_year(structure):
    if structure is not None:
        return structure.schoolyear_set.filter(is_active=True).last() if structure.schoolyear_set.filter(is_active=True).count() != 0 else None
    else:
        return None


def list_to_queryset(model: ModelBase, data: list) -> models.QuerySet:
    if not isinstance(model, ModelBase):
        raise ValueError(f"{model} must be Model")
    if not isinstance(data, list):
        raise ValueError(f"{data} must be List Object")

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)


def queryset_fusion(
    q1: models.QuerySet, q2: models.QuerySet, model: ModelBase
) -> models.QuerySet:
    result_list = list(chain(list(q1), list(q2)))
    return list_to_queryset(model, result_list).distinct()


def querysets_fusion(querysets_list: list[QuerySet], model: ModelBase) -> models.QuerySet:
    data = []
    for querysets in querysets_list:
        for q in querysets:
            if q not in data:
                data.append(q)
    return list_to_queryset(model, data).distinct()


def custom_paginator(request, queryset: models.QuerySet, number: int):
    paginator = Paginator(queryset, number)
    page = request.GET.get("page")
    return paginator.get_page(page), paginator.page_range


def convert_money_to_int(money: str) -> int:
    if money.split(".")[1] != 0:
        return int(money.split(".")[0])
    return int(float(money) * 100)


def generate_serie(n):
    serie = ""
    for _ in range(n):
        # Génère un chiffre aléatoire entre 0 et 9
        chiffre = random.randint(1, 9)
        serie += str(chiffre)
    return serie


def sorted_evaluations_data(data: dict):
    data_keys_sorted = sorted(data.keys(), key=lambda x: (
        0 if x.startswith("Interrogation") else
        1 if x.startswith("Devoir") else
        2 if x.startswith("Examen") else
        3 if x.startswith("Examen de") else
        4 if x.startswith("Moyenne") else 5
    ))
    return data_keys_sorted


def sorted_timetable_data(data: dict):
    data_keys_sorted = sorted(data.keys(), key=lambda x: (
        0 if x.startswith("Lundi") else
        1 if x.startswith("Mardi") else
        2 if x.startswith("Mercredi") else
        3 if x.startswith("Jeudi") else
        4 if x.startswith("Vendredi") else
        5 if x.startswith("Samedi") else
        6 if x.startswith("Dimanche") else 7
    ))
    return data_keys_sorted


def sorted_days(days: list):
    order_days = ["Lundi", "Mardi", "Mercredi",
                  "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    # Trier la liste des jours de la semaine en fonction de l'ordre spécifié
    sorted_days = sorted(days, key=lambda x: order_days.index(x))

    return sorted_days


def sorted_list_data(days: list, order: list):
    # Trier la liste des jours de la semaine en fonction de l'ordre spécifié
    sorted_days = sorted(days, key=lambda x: order.index(x))

    return sorted_days


def generate_excel_font(font_name: str, font_size: int, font_color: str = "black", bold: bool = False):
    font_style = xlwt.XFStyle()
    font_style.font.bold = bold
    font_style.font.name = font_name
    font_style.font.height = font_size * 20
    font_style.colour_index = xlwt.Style.colour_map[f'{font_color}']

    return font_style


def parsing_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d").date()


def custom_datetime_combine(date: datetime):
    return datetime.strftime(date, "%d/%m/%Y %H:%M")


def extract_dates_from_datas(class_attendances: models.QuerySet):
    return set([attendance.date for attendance in class_attendances])


def is_after_today(date: date):
    if date > date.today():
        return True
    return False


def duration_since_start_to_end(start_time, end_time):
    return end_time - start_time


def duration_since_start_to_end__seconds(start_time, end_time):
    return duration_since_start_to_end(start_time, end_time).seconds


def duration_since_start_to_end__minutes(start_time, end_time):
    return duration_since_start_to_end__seconds(start_time, end_time) // 60


def hours_duration(start_time, end_time):
    return duration_since_start_to_end__minutes(start_time, end_time) // 60


def generate_structure_qr_code(structure, title, admission_application_url):
    # Création d'un objet QRCode avec les paramètres spécifiés
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    # Ajout de l'URL de demande d'admission aux données du QRCode
    qr.add_data(admission_application_url)
    qr.make(fit=True)

    # Création de l'image QRCode avec les couleurs spécifiées
    img = qr.make_image(fill_color=(0, 0, 102), back_color=(204, 119, 34))

    # Conversion de l'image PIL en un objet BytesIO
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)  # Remettre le curseur au début du fichier BytesIO

    if settings.DEFAULT_FILE_STORAGE == 'cloudinary_storage.storage.MediaCloudinaryStorage':
        from cloudinary.uploader import upload
        # Téléchargement de l'image sur Cloudinary
        response = upload(img_io, folder='jool/image/saqc',
                          public_id=f'{structure.short_name}_saqc')
        image_url = response.get('secure_url')

        # Mise à jour de l'URL de l'image dans le champ admission_qr_code de l'objet structure
        if image_url:
            # Mise à jour du champ admission_qr_code de l'objet structure avec l'URL de l'image
            structure.admission_qr_code = f"image/saqc/{structure.short_name}_saqc.png"
    else:
        # Utiliser le stockage local en développement
        img_file = File(img_io, name=f'{structure.short_name}_saqc.png')
        structure.admission_qr_code.save(
            f'{structure.short_name}_saqc.png', img_file, save=True)

    structure.save(update_fields=['admission_qr_code'])


def extract_cycles_subs(cycles, CycleModel):
    data_s = []
    for cycle in cycles:

        if CycleModel.objects.filter(parent=cycle).exists() is True:
            for sub_cycle in CycleModel.objects.filter(parent=cycle):
                if sub_cycle not in data_s:
                    data_s.append(sub_cycle)

    return list_to_queryset(CycleModel, data_s)


def attribuer_mention(moyenne):
    if moyenne >= 16:
        return "Très Bien"
    elif 14 <= moyenne < 16:
        return "Bien"
    elif 12 <= moyenne < 14:
        return "Assez Bien"
    elif 10 <= moyenne < 12:
        return "Passable"
    elif 8 <= moyenne < 10:
        return "Insuffisant"
    elif 6 <= moyenne < 8:
        return "Très Insuffisant"
    else:
        return "Médiocre"


def generate_unique_invoice_code(length):
    # 1. Créer un UUID unique basé sur le temps et l'ID unique
    unique_id = str(uuid.uuid4())

    # 2. Ajouter un timestamp pour encore plus d'unicité
    timestamp = str(int(time.time()))

    # 3. Combiner UUID et timestamp
    raw_code = unique_id + timestamp

    # 4. Générer un hash SHA-256 pour obtenir une chaîne de longueur fixe
    hash_object = hashlib.sha256(raw_code.encode('utf-8'))
    unique_code = hash_object.hexdigest()

    # 5. Limiter la longueur à 50 caractères
    return unique_code[:length]


def get_weeks_in_month(year, month):
    """
    Divise un mois en semaines (lundi à dimanche).
    :param year: Année (int)
    :param month: Mois (int)
    :return: Liste de tuples contenant les plages de dates pour chaque semaine.
    """
    # Obtenir le premier et le dernier jour du mois
    first_day = date(year, month, 1)
    last_day = date(year, month + 1, 1) - \
        timedelta(days=1) if month < 12 else date(year, month, 30)

    # Initialiser la liste des semaines
    weeks = []

    # Trouver le premier lundi avant ou égal au premier jour du mois
    current_start = first_day - timedelta(days=first_day.weekday())

    while current_start <= last_day:
        # Calculer la fin de la semaine
        current_end = current_start + timedelta(days=6)

        # Assurer que la semaine reste dans le mois
        week_start = max(current_start, first_day)
        week_end = min(current_end, last_day)

        # Ajouter la semaine à la liste
        weeks.append((week_start, week_end))

        # Passer à la semaine suivante
        current_start = current_start + timedelta(days=7)

    return weeks


class FieldChangeDetectorMixin:
    """
    Mixin pour détecter les changements de champs dans un modèle Django.
    """

    def has_field_changed(self, field_name):
        """
        Vérifie si un champ donné a changé.
        """
        if not self.pk:
            return False  # Nouveau modèle, aucune modification possible
        old_value = getattr(self.__class__.objects.get(pk=self.pk), field_name)
        new_value = getattr(self, field_name)
        return old_value != new_value


def formating_float(value: float) -> str:
    return int(value) if value.is_integer() else value


def encode_to_four_chars(input_string) -> str:
    # Assurer que la chaîne est bien une chaîne de caractères
    input_string = str(input_string)
    # Ajouter des zéros au début jusqu'à obtenir une longueur de 4
    return input_string.zfill(4)
