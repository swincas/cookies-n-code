---
author: Robert A. Mostoghiu Paun
tags:
  - tutorial
---
# Zotero configuration
1. Download *Zotero* and *Zotero Connector* from [here](https://www.zotero.org/download/). Zotero Connector allows us to add papers from ADS, Arxiv, etc. directly to our Zotero library by simply clicking on a button from the browser.
2. Install the following addons for Zotero:
	1.  *Zotfile*, by following the steps described [here](https://zotfile.com/#how-to-install--set-up-zotfile)
	2. *Better Bibtex*, by following the steps described [here](https://retorque.re/zotero-better-bibtex/installation/index.html)
3. Most of the configuration for Zotero and Zotfile can be found  in the following [link](https://habr.com/en/articles/443798/). There are, however, some settings I changed because of personal preference. In particular, I prefer to organise my library by (main) author and then, for the same author, by year, and prefer some different rules for renaming pdfs once added to the library. Feel free to experiment with the syntax.

![[screenshots/zotero_obsidian_tut9.png]]

![[screenshots/zotero_obsidian_tut10.png]]

4. For Better BibTex, I set it so that papers added to my library get automatically a citation key following a certain syntax (feel free to change it). When Obsidian is called to read the Zotero information, the Obsidian note is renamed to the citation key assigned by Better BibTex. **Note** the settings for Better Bibtex are in Zotero Settings.

![[screenshots/zotero_obsidian_tut11.png]]

# Obsidian configuration
1. Download Obsidian from [here](https://obsidian.md/download). Obsidian stores all your notes in “vaults”, local directories in your computer. Create a new vault.
2. Create a new folder in your vault (e.g. “<your_vault_name>/templates”) that will store your Zotero template, a file which tells Obsidian how to handle the information scraped from Zotero. In my case, I saved the following template in a file called “zotero_papers_template” and I saved it it the templates folder (i.e. <your_vault_name>/templates/zotero_papers_template) :

```
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

```

3. In Settings → Appearance scroll all the way down to “CSS snippets” and click on the folder icon to open the folder in which we will add a file telling Obsidian how to handle the colors in the Zotero template. Save the following in a file (e.g. “zotero_obsidian_colors.css“) and move it to that folder:

```
/* Yellow */
.callout[data-callout-metadata="#ffd400"] {
  --callout-color: 255, 204, 0;
}

/* Red */
.callout[data-callout-metadata="#ff6666"] {
  --callout-color: 255, 59, 48;
}

/* Green */
.callout[data-callout-metadata="#5fb236"] {
  --callout-color: 40, 205, 65;
}

/* Blue */
.callout[data-callout-metadata="#2ea8e5"] {
  --callout-color: 0, 122, 255;
}

/* Purple */
.callout[data-callout-metadata="#a28ae5"] {
  --callout-color: 125, 84, 222;
}
```

![[screenshots/zotero_obsidian_tut5.png]]

**Note**: once copied to the folder you can press the refresh button and it should appear in Obsidian as a toggeable snippet. Don’t forget to activate the snippet!

5. Install the plugin *Zotero Integration* (Settings → Community plugins \[Browse])

![[screenshots/zotero_obsidian_tut1.png]]

4. Set the following in the settings of *Zotero Integration* (Settings → Zotero Integration):

	1.  Install the PDF utility 
	
	![[screenshots/zotero_obsidian_tut2.png]]
	
	2. Set Database to “Zotero”
	
	![[screenshots/zotero_obsidian_tut3.png]]
	
	3. Create a new type of Citation Format by clicking on “Add Citation Format“, call it whatever you want (e.g. “Citation”) and set it as a “Formatted Citation” with the style you prefer. In my case I chose ApJ. Whichever style you pick you will have to have support for such style in Zotero too. Citation styles can be added to Zotero by following [this link](https://www.zotero.org/support/styles) 
	
	![[screenshots/zotero_obsidian_tut6.png]]
	
	4. Create a new Import Format by clicking on “Add Import Format”. Give it a name (e.g “Paper”), and select the directory in which you want to save new notes imported from Zotero. In my case I wanted to store them in a separate folder in my vault called “papers”, and I wanted to automatically name such notes by the citation key they have assigned, hence I picked “papers/{{citekey}}.md“). I personally also want the images obtained from Zotero notes to be stored in separate folder so it does not clutter my papers folders, thus I picked “images/{{citekey}}/” as the path. **Note**: the folders “papers” and “images” have to be created in the vault first.
	
	![[screenshots/zotero_obsidian_tut7.png]]
	
	5. Select the template file we created before to tell Obsidian it should use that format when pulling information from Zotero. Finally, choose the bibliography style for this format (I choose the same style as before, ApJ).
	
	![[screenshots/zotero_obsidian_tut8.png]]

# Making it work
If Zotero and Obsidian are correctly configured, after the highlighting, adding notes, selecting parts of a pdf, etc. in Zotero we can automatically export that information to an Obsidian note by invoking the Zotero Integration plugin from the Command Palette (i.e. ``CMD + P`` on Mac, ``CTRL + P`` on Windows) and selecting *Zotero Integration: Paper*, i.e. the new Import Formats we created.

![[screenshots/zotero_obsidian_tut12.png]]

A new prompt will appear, in which we will type either the name of the paper we want to import or its citation key (the citation key can be checked in the metadata of the paper in Zotero)

![[screenshots/zotero_obsidian_tut13.png]]

If the configuration was successful, a new note named after the paper’s citation key will appear in the directory we picked as the default location for the Obsidian notes created from Zotero papers.

![[screenshots/zotero_obsidian_tut14.png]]

The template supports the following colors in Zotero:
1. Red → Negative
2. Green → Positive
3. Teal → Motivation
4. Purple → Key Results
5. Yellow → Highlights

Feel free to change the template, but I suggest making a backup before you change anything :)

# Extra plugins I recommend
These are some of the plugins I use. Maybe you would want to use them too. 
All of them can be found in the Community Plugins section of the Obsidian settings.
* *Calendar* + *Periodic Notes*: very useful for creating daily, weekly, and monthly notes firectly by clicking on the calendar. 
* *Dataview*: essentially SQL for creating custom tables and indexing the notes coming from Zotero papers. I personally have a note called “0_papers_index“ that acts as a summary of the notes I created from Zotero. If the plugin is installed, the following code should do just that:
```dataview
TABLE file.aliases[0] AS Title, file.cday as "Date Created"
WHERE contains(file.tags, "#papers") AND !contains(file.name, "zotero_papers") AND !contains(file.name, "0_papers_index")
SORT file.name asc
```
* *Excalidraw*: if you ever need to draw things and add them to notes, this is the plugin. It’s very complex but intuitive to use. No need to watch all the video tutorials available on it.
* *Git*: essential for backing up your vault(s)! Obsidian stores the files created **locally**! This plugin allows us to commit the changes to our vault and do the usual version control tricks to it.
* *Plugin Update Tracker*: automatically checks if there is any update to the plugins installed and shows a prompt if updates are available. **Note** it does not check for theme updates!
* *Style Settings*: essential plugin for changing settings of themes we download.
* *Templater*: we can assign hotkeys to templates and have templates run on startup of Obsidian.
* *Better Word Count*: if counting the amounts of words and characters is ever required for a project… I guess.
* *Natural Language Dates*: add dates to notes using syntax like “today” and “yesterday”.
