from django import template
from django.utils.safestring import mark_safe

from menu.models import Menu, MenuItem


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name=None):
    """Кастомный тег для отрисовки одного или всех меню"""
    request = context['request']
    current_url = request.path

    menus = Menu.objects.all()
    if menu_name:
        menus = menus.filter(name=menu_name)

    if not menus.exists():
        return ""

    def render_menu(menu):
        all_items = MenuItem.objects.filter(menu=menu).select_related('parent')
        children_map = {}

        for item in all_items:
            children_map.setdefault(item.parent_id, []).append(item)

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

                if item.id in children_map:
                    html += render_items(item.id, level + 1, active_branch_ids)

                html += '</li>'
            html += '</ul>'
            return html

        active_branch_ids = find_active_branch()
        return f"<h4>{menu.name}</h4>" + render_items(
            None, 0, active_branch_ids
        )

    return mark_safe("".join(render_menu(menu) for menu in menus))
