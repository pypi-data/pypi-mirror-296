<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
      % if not title is UNDEFINED:
        <title>${title}</title>
      % else:
        <title>MoOGLi</title>
      % endif
      <link rel="apple-touch-icon" sizes="180x180" href="${request.static_url('caerp:static/favicons/apple-touch-icon.png')}">
      <link rel="icon" type="image/png" sizes="32x32" href="${request.static_url('caerp:static/favicons/favicon-32x32.png')}">
      <link rel="icon" type="image/png" sizes="16x16" href="${request.static_url('caerp:static/favicons/favicon-16x16.png')}">
      <link rel="manifest" href="${request.static_url('caerp:static/favicons/site.webmanifest')}">
      <link rel="mask-icon" href="${request.static_url('caerp:static/favicons/safari-pinned-tab.svg')}" color="#000000">
      <link rel="shortcut icon" href="${request.static_url('caerp:static/favicons/favicon.ico')}">
      <meta name="msapplication-TileColor" content="#2b5797">
      <meta name="msapplication-config" content="${request.static_url('caerp:static/favicons/browserconfig.xml')}">
      <meta name="theme-color" content="#ffffff">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="robots" content="noindex">
    </%block>
  </head>
  <body class="caerp theme_default ${request.matched_route.name}-view">
    <div class="layout flex two_cols third">
      <main class="login_form flex">
        <div class="logos">
          <div class="flex">
            <img src="${request.static_url('caerp:static/img/logo.png')}" alt="CAERP" class="caerp_logo">
            <img src="/public/logo.png" alt="Logo de ${request.config.get('cae_business_name', ' ')}" class="cae_logo" />
          </div>
        </div>
		<h1 class="screen-reader-text">Identification</h1>
        <%block name='pop_message'>
        % for message in request.session.pop_flash(queue=""):
          % if message is not None:
            <div class='row hidden-print'>
            <div class='col-md-6 col-md-offset-3'>
              <div class="alert alert-success">
                <button class="icon only unstyled close" title="Masquer ce message" aria-label="Masquer ce message" data-dismiss="alert" type="button"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg></button>
                <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#success"></use></svg></span>
                ${api.clean_html(message)|n}
              </div>
            </div>
          </div>
          % endif
        % endfor
        % for message in request.session.pop_flash(queue="error"):
          % if message is not None:
            <div class='row hidden-print'>
            <div class='col-md-6 col-md-offset-3'>
              <div class="alert alert-danger">
                <button class="icon only unstyled close" title="Masquer ce message" aria-label="Masquer ce message" data-dismiss="alert" type="button"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg></button>
                <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#danger"></use></svg></span>
                ${api.clean_html(message)|n}
              </div>
            </div>
          </div>
          % endif
        % endfor
        </%block>
        <%block name='content' />
        <div class="login_footer">
            <p>Pour<br /><strong>${request.config.get("cae_business_name", " ")}</strong></p>
            <p>Par<br /><a href="https://framagit.org/caerp/caerp"><strong>l'Équipe CAERP</strong></a></p>
        </div>
        <footer id='page-footer-block'>
            MoOGLi ${layout.caerp_version}
            <%block name='footer' />
        </footer>
      </main>
      <aside class="atwork_photo"></aside>
    </div>

    <script type='text/javascript'>
      $( function() {
        $.getJSON("${request.route_path('login_photos')}", function(json) {
          var photos = JSON.parse(JSON.stringify(json));
          var i = Math.floor(Math.random()*photos.length);
          var photo_tag = "<p>";
          if(photos[i]["title"]!="") photo_tag += "<strong>"+photos[i]["title"]+"</strong>";
          if(photos[i]["subtitle"]!="") photo_tag += "<br />"+photos[i]["subtitle"];
          if(photos[i]["author"]!="") photo_tag += "<br /><small>Photo&nbsp;: <em>"+photos[i]["author"]+"</em></small>";
          photo_tag += "</p>";
          $('.atwork_photo').html(photo_tag);
          $('.atwork_photo').attr("style", "background-image:url('" + photos[i]["photo"]["preview_url"] + "')");
        });
      });
    </script>

  </body>
</html>
