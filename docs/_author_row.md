{% set authors = page.meta.authors if page.meta.authors is defined else [page.meta.author] %}
<span style="display: flex; align-items: center; font-size: 0.98em;">
  {% for auth in authors -%}
    <img src="{{ get_avatar(auth) }}" width="32" height="32" style="border-radius:50%; margin-right: 0.5em;"><strong>{{ auth }}</strong>{% if not loop.last %}<span style="margin: 0 0.5em;"> </span>{% endif %}
  {%- endfor %}
  <span style="margin: 0 0.5em;">·
    <small style="color: #888;">
      :material-clock-edit-outline: Last updated: {{ git_revision_date_localized }}
    </small>
  </span>
</span>