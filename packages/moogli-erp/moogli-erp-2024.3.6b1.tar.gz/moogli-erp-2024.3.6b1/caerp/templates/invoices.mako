<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/searchformlayout.mako" import="searchform"/>

<%block name='actionmenucontent'>
<div class='layout flex main_actions'>
    ${request.layout_manager.render_panel('action_buttons', links=stream_main_actions())}
    ${request.layout_manager.render_panel(
      'menu_dropdown',
      label="Exporter",
      links=stream_more_actions(),
      display_label=True,
      icon="file-export",
    )}
</div>
</%block>

<%block name='content'>

${searchform()}

<div>
    <div>
        ${records.item_count} Résultat(s)
    </div>
    <div class='table_container'>
        ${request.layout_manager.render_panel('task_list', records, datatype="invoice", is_admin_view=is_admin)}
    </div>
    ${pager(records)}
</div>
</%block>
