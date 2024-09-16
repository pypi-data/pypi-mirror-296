"""Utility views or functions used everywhere"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from esi.decorators import token_required

from allianceauth.eveonline.models import EveCorporationInfo
from app_utils.allianceauth import notify_admins

from metenox import tasks
from metenox.app_settings import METENOX_ADMIN_NOTIFICATIONS_ENABLED
from metenox.models import ESI_SCOPES, HoldingCorporation, Moon, Owner


def add_common_context(context: dict = None) -> dict:
    """Enhance the templates context with context that should be added to every page"""
    if context is None:
        context = {}

    if basic_title := context.get("page_title"):
        context["page_title"] = f"{basic_title} - Metenox"
    else:
        context["page_title"] = "Metenox"

    context["monthly_fuel_price"] = Moon.fuel_price()

    return context


@cache_page(3600)
def modal_loader_body(request):
    """Draw the loader body. Useful for showing a spinner while loading a modal."""
    return render(request, "metenox/modals/loader_body.html")


@permission_required(["metenox.basic_access"])
@token_required(scopes=ESI_SCOPES)
@login_required
def add_owner(request, token):
    """Render view to add an owner."""
    character_ownership = get_object_or_404(
        request.user.character_ownerships.select_related("character"),
        character__character_id=token.character_id,
    )
    corporation_id = character_ownership.character.corporation_id
    try:
        corporation = EveCorporationInfo.objects.get(corporation_id=corporation_id)
    except EveCorporationInfo.DoesNotExist:
        corporation = EveCorporationInfo.objects.create_corporation(
            corp_id=corporation_id
        )
        corporation.save()

    holding_corporation, _ = HoldingCorporation.objects.get_or_create(
        corporation=corporation,
    )

    owner, created = Owner.objects.get_or_create(
        corporation=holding_corporation, character_ownership=character_ownership
    )
    if not created:
        owner.enable()  # Gives another chance to the toon at being used for updates

    # TODO figure out why I need to type all this to get the right corp id
    tasks.update_holding.delay(owner.corporation.corporation.corporation_id)
    messages.success(request, f"Update of refineries started for {owner}.")
    if METENOX_ADMIN_NOTIFICATIONS_ENABLED:
        notify_admins(
            message=f"{owner} was added as new owner by {request.user}.",
            title=f"Metenox: Owner added: {owner}",
        )
    return redirect("metenox:corporations")
