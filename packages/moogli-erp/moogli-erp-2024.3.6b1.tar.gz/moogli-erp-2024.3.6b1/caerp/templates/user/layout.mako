<%inherit file="/layouts/default.mako" />
<%namespace file="/base/utils.mako" import="format_mail" />

<%block name="headtitle">
% if title is not UNDEFINED and title is not None:
    <h1>
        ${title}
        % if title_detail is not UNDEFINED and title_detail is not None:
            <small> ${title_detail}</small>
        % endif
    </h1>
% endif
</%block>

<%block name='content'>
<div class='data_display separate_block content_padding limited_width width40 user_header'>
	<div class='layout flex'>
        <span class='user_avatar'>
            % if layout.current_user_object.photo_file:
                <img src="${api.img_url(layout.current_user_object.photo_file)}" 
                    title="${api.format_account(layout.current_user_object)}" 
                    alt="Photo de ${api.format_account(layout.current_user_object)}" 
                    width="256" height="256" />
            % else:
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#user"></use></svg>
            % endif
        </span>
        <div>
            <h2>
                % if layout.current_user_object.civilite:
                    ${api.format_civilite(layout.current_user_object.civilite)}&nbsp;
                % endif
                ${api.format_account(layout.current_user_object)}
            </h2>
			<p>
				${format_mail(layout.current_user_object.email)}
			</p>
			<p>
                % if layout.current_user_object.userdatas and layout.current_user_object.userdatas.situation_situation:
                 <strong>${layout.current_user_object.userdatas.situation_situation.label}</strong>
                % endif
 			</p>
 			<p>
                % if layout.current_user_object.userdatas and layout.current_user_object.userdatas.situation_societariat_entrance:
                <strong class="highlight">Sociétaire</strong>
                % endif
 			</p>
       </div>
       <div>
			% if request.has_permission("edit.user", layout.current_user_object):
			<a class='btn icon only' href="${request.route_path('/users/{id}/edit', id=layout.current_user_object.id)}" title="Modifier l’utilisateur" aria-label="Modifier l’utilisateur">
				<svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#pen"></use></svg>
			</a>
			% endif
       </div>
    </div>
</div>
<div class='layout flex two_cols quarter'>
    <div class='sidebar-container'>
		<%block name='rightblock'>
			${request.layout_manager.render_panel('sidebar', layout.usermenu)}
		</%block>
	</div>
    <div class='tab-content'>
        <%block name='mainblock' />
    </div>
</div>
</%block>