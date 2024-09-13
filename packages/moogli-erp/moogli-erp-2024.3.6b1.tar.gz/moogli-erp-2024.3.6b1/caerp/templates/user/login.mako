<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" name="utils"/>
<%block name="mainblock">
% if login is None:
<div class='alert alert-warning'>
    <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#exclamation-circle"></use></svg></span>
    Ce compte ne dispose pas d’identifiant pour se connecter à MoOGLi
</div>
<a
    class='btn btn-primary'
    href="${request.route_path('/users/{id}/login/add', id=request.context.id)}"
>
    <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#plus"></use></svg>Créer des identifiants pour ce compte
</a>
% else:
<div class='user_dashboard'>
    % if request.has_permission('edit.login'):
	<div class='separate_bottom'>
		Nom d’utilisateur <strong>${login.login}</strong>
		% if login.active:
		<div class='alert alert-success'>
			<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#check"></use></svg></span>
			Cet identifiant est actif
		</div>
		% else:
		<div class='alert alert-danger'>
			<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg></span>
			Cet identifiant n’est pas actif
		</div>
	% endif
        <p>Fait partie des groupes</p>
        <ul class="content_padding">
        % for group in login._groups:
        <li>${group.label}</li>
        % endfor
        </ul>
        <p>Montants maximum autorisés pour l'autovalidation</p>
        <ul>
            <li>Devis : ${utils.show_amount_or_undefined_string(login.estimation_limit_amount)}</li>
            <li>Factures : ${utils.show_amount_or_undefined_string(login.invoice_limit_amount)}</li>
            <li>Commandes fournisseur : ${utils.show_amount_or_undefined_string(login.supplier_order_limit_amount)}</li>
            <li>Factures fournisseur : ${utils.show_amount_or_undefined_string(login.supplier_invoice_limit_amount)}</li>
        </ul>
        <% activate_url = request.route_path('/logins/{id}', id=login.id, _query={'action': 'activate'}) %>
        % if login.active:
        <a
            href="${request.route_path('/users/{id}/login/edit', id=login.user_id)}"
            class='btn'
            title='Modifier identifiant, mot de passe, groupes'
            aria-label='Modifier identifiant, mot de passe, groupes'
            >
            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#pen"></use></svg>
            Modifier
        </a>

        <%utils:post_action_btn url="${activate_url}" icon="lock"
        _class="btn btn-danger"
        title="Désactiver ce compte (cet utilisateur ne pourra plus se connecter)"
        >
            Désactiver ce compte
        </%utils:post_action_btn>
        % else:
        <%utils:post_action_btn url="${activate_url}" icon="check"  _class="btn">
            Activer
        </%utils:post_action_btn>
        % endif

    % elif request.has_permission('set_password.login'):
        <a
            href="${request.route_path('/users/{id}/login/set_password', id=_context.id)}"
            class='btn btn-primary'
            >
            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#lock"></use></svg>
            Changer mon mot de passe
        </a>
    % endif
	</div>
% endif
</%block>
