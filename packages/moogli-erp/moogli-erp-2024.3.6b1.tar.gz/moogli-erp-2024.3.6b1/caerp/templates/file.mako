<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" name="utils" />

<%def name="display_actions()">
	<div class='layout flex main_actions'>
		<div role='group'>
			<a class='btn btn-primary' href="${download_url}" title="Télécharger ce fichier" aria-label="Télécharger ce fichier">
				<svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#download"></use></svg>
				Télécharger
			</a>
			% if request.has_permission('edit.file', file):
				<a class='btn' href="${edit_url}" title="Modifier ce fichier" aria-label="Modifier ce fichier">
					<svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#pen"></use></svg>
					Modifier
				</a>
			% endif
			% if request.has_permission('delete.file', file):
				<%utils:post_action_btn url="${delete_url}" icon="trash-alt" _class="btn negative"
					onclick="return confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')"
					title="Supprimer définitivement ce fichier"
					aria_label="Supprimer définitivement ce fichier"
				>
					Supprimer
				</%utils:post_action_btn>
			% endif
		</div>
	</div>
</%def>

<%block name='actionmenucontent'>
% if navigation and not request.is_popup:
	<div class="container-fluid local-navigation">
		<ul class="breadcrumb breadcrumb-arrow">
			<li><a href="${navigation.url}">${navigation.title}</a></li>
		</ul>
	</div>
% endif
% if not request.is_popup:
	${display_actions()}
% endif
</%block>

<%block name='content'>
% if request.is_popup:
	${display_actions()}
% endif
<div class='popup_content'>
	<dl class='dl-horizontal'>
		<dt>Description du fichier</dt><dd>${file.description}</dd>
		<dt>Nom du fichier</dt><dd> ${file.name}</dd>
		<dt>Taille du fichier</dt><dd>${api.human_readable_filesize(file.size)}</dd>
		<dt>Date de dépôt</dt><dd>${api.format_date(file.created_at)}</dd>
		<dt>Dernière modification</dt><dd>${api.format_date(file.updated_at)}</dd>
	</dl>
</div>
</%block>
