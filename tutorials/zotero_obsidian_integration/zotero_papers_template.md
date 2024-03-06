---
author: Robert A. Mostoghiu Paun
tags: " #papers"
aliases: [" {{title}}"]
---
{#-**Macro for giving meaning to different highlighting colours**-#}
{%- macro colorValueToName(color) -%}
	{%- switch color -%}
		{%- case "#ff6666" -%} {#-**Red**-#}
			Negative
		{%- case "#5fb236" -%} {#-**Green**-#}
			Positive
		{%- case "#2ea8e5" -%} {#-**Teal**-#}
			Motivation
		{%- case "#a28ae5" -%} {#-**Purple**-#}
			Key Results
		{%- default -%} {#-**Yellow**-#}
			Highlights
	{%- endswitch -%}
{%- endmacro -%}

{#-**Macro for classifying different annotation types**-#}
{%- macro calloutHeader(type) -%}
	{%- switch type -%}
		{%- case "highlight" -%}
			…
		{%- case "strike" -%}
			Strikethrough
		{%- case "underline" -%}
			Underline
		{%- case "image" -%}
			Image
		{%- default -%}
			Note
	{%- endswitch -%}
{%- endmacro %}

# Paper Details

>[!note]  @{{citekey}}
> **Title**: **{{title}}**
> 
> **Author(s)**: {% for creator in creators %} {% if creator.name == null %} {{creator.lastName}}, {{creator.firstName}}; {% endif %}{% if creator.name %} {{creator.name}}{% endif -%}{% endfor %}   
> 
> **Date**: {{date | format("DD-MM-YYYY")}}
> 
{%- if itemType == "journalArticle" %}
> **Journal**: *{{publicationTitle}}* 
{%- endif %}
{%- if itemType == "bookSection" %}
> **Book**: {{publicationTitle}} 
{%- endif %}
{%- if publisher %}
> **Publisher**: {{publisher}} 
{%- endif %}
{%- if DOI %}
> **DOI**: {{DOI}} 
{%- endif %}
{%- if ISBN %}
> **ISBN**: {{ISBN}} 
{%- endif %}
{%- if bibliography %} 
> **Citation**: {{bibliography}} 
{%- endif %}
>
> **Links**: [**Publisher Online**]({{url}}) [**Zotero Local**]({{desktopURI}}) {%- for attachment in attachments | filterby("path", "endswith", ".pdf") %} [**Original PDF**](file://{{attachment.path | replace(" ", "%20")}}){% if loop.last %}{% endif %}{%- endfor %}

> [!Abstract]  
> {{abstractNote}}  


# Annotations
{% persist "annotations" %}
{% set annots = annotations | filterby("date", "dateafter", lastImportDate) -%}
{% if annots.length > 0 %}
Imported on {{importDate | format("YYYY-MM-DD h:mm a")}}

{% for color, annots in annots | groupby("color") -%}
#### {{colorValueToName(color)}}

{% for annot in annots -%}

>[!quote{% if annot.color %}|{{annot.color}}{% endif %}] [Page {{annot.page}}](zotero://open-pdf/library/items/{{annot.attachment.itemKey}}?page={{annot.page}})
{%- if annot.annotatedText %}
> 	{{annot.annotatedText | nl2br}}
{%- endif -%}
{%- if annot.imageRelativePath %}
> 	![[{{annot.imageRelativePath}}]]
{%- endif %}
{%- if annot.ocrText %}
> 	{{annot.ocrText}}
{%- endif %}
{%- if annot.comment %}
>
>>{{annot.comment | nl2br}}
>{%- endif %}

{% endfor -%}
{% endfor -%}
{% endif %}
{% endpersist %}
