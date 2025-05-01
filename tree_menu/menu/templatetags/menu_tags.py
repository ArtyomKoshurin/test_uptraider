from django import template
from django.urls import resolve, Resolver404
from django.utils.safestring import mark_safe

from menu.models import Menu, MenuItem


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name=None):
    request = context['request']
    current_url = request.path
    menus = Menu.objects.filter(
        name=menu_name
    ) if menu_name else Menu.objects.all()

    if not menus.exists():
        return ""

    def render_menu(menu):

        all_items = MenuItem.objects.filter(menu=menu).select_related('parent')
        children_map = {}
        for item in all_items:
            children_map.setdefault(item.parent_id, []).append(item)

        def is_active(item):
            item_url = item.get_url()
            if not item_url or item_url == '#':
                return False
            if current_url == '/':
                return item_url == '/' or item_url == ''

            return current_url == item_url or current_url.startswith(
                item_url + '/'
            )

        def find_active_item():

            for item in all_items:
                if is_active(item):
                    return item

            try:
                resolved = resolve(current_url)
                for item in all_items:
                    if item.named_url and item.named_url == resolved.url_name:
                        return item
            except Resolver404:
                pass
            return None

        active_item = find_active_item()
        active_branch_ids = set()
        first_level_children = set()

        if active_item:

            item = active_item
            while item:
                active_branch_ids.add(item.id)
                item = item.parent

            for child in children_map.get(active_item.id, []):
                first_level_children.add(child.id)

        def render_items(parent_id=None, level=0):
            html = "<ul>"
            for item in sorted(
                children_map.get(parent_id, []), key=lambda x: x.title
            ):
                is_item_active = active_item and item.id == active_item.id
                in_active_branch = item.id in active_branch_ids
                is_first_level_child = item.id in first_level_children

                should_expand = is_item_active or in_active_branch or is_first_level_child

                css_class = "active" if is_item_active else "open" if in_active_branch or is_first_level_child else ""
                html += f'<li class="{css_class}"><a href="{item.get_url()}">{item.title}</a>'

                if should_expand or not active_item:
                    html += render_items(item.id, level + 1)
                html += '</li>'
            html += '</ul>'
            return html

        return f"<h4>{menu.name}</h4>" + render_items(None)

    return mark_safe("".join(render_menu(menu) for menu in menus))
