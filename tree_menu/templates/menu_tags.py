from django import template
from django.utils.safestring import mark_safe

from menu.models import Menu, MenuItem


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return mark_safe(f"<p>Меню '{menu_name}' не найдено.</p>")

    all_items = MenuItem.objects.filter(menu=menu).select_related('parent')
    children_map = {}

    for item in all_items:
        children_map.setdefault(item.parent_id, []).append(item)

    request = context['request']
    current_url = request.path

    def is_active(item):
        return item.get_url() == current_url

    def find_active_branch():
        for item in all_items:
            if is_active(item):
                branch = set()
                while item:
                    branch.add(item.id)
                    item = item.parent
                return branch
        return set()

    def render_items(parent_id=None, level=0, active_branch_ids=None):
        html = "<ul>"
        for item in children_map.get(parent_id, []):
            active = is_active(item)
            in_active_branch = active_branch_ids and item.id in active_branch_ids

            css_class = "active" if active else "open" if in_active_branch else ""
            html += f'<li class="{css_class}"><a href="{item.get_url()}">{item.title}</a>'

            if active or in_active_branch or (
                active_branch_ids and item.id in active_branch_ids
            ):
                html += render_items(item.id, level + 1, active_branch_ids)
            html += '</li>'
        html += '</ul>'
        return html

    active_branch_ids = find_active_branch()
    tree_html = render_items(
        parent_id=None,
        level=0,
        active_branch_ids=active_branch_ids
    )

    return mark_safe(tree_html)
