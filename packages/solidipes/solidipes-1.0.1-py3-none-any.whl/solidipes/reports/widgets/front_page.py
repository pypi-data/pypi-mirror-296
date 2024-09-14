from .solidipes_buttons import SolidipesButtons as SPB
from .solidipes_logo_widget import SolidipesLogoWidget as SPLW

################################################################


class FrontPage(SPLW):
    def __init__(self, **kwargs):
        super().__init__(
            title="""
        <center>

# Welcome to the Solidipes Curation Tool!
        """,
            width="15%",
            **kwargs,
        )

        buttons_custom_style = {
            "grid-column": 1,
            "width": "100%",
        }
        self.layout.html(
            f"""
<style>
    .steps-container {{
        align-items: center;
        gap: 1rem;
        grid-template-columns: 8rem 1fr;
        max-width: 55rem;
    }}

    .steps-text {{
        grid-column: 2;
        margin-bottom: 1rem;
        text-align: left;
    }}

    @media all and (min-width: 680px) {{
        .steps-container {{
            display: grid;
        }}

        .steps-text {{
            margin-bottom: 0;
        }}
    }}
</style>
<center>
    <h3 style="margin-bottom: 1rem;">Here, you can prepare your paper’s data for publication in four steps:</h3>

    <div class="steps-container">
        {SPB()._html_link_button("Acquisition", "?page=acquisition", custom_style=buttons_custom_style)}
        <div class="steps-text">Upload any files relevant to your paper, and browse them like you would in a file
        browser.</div>

        {SPB()._html_link_button("Curation", "?page=curation", custom_style=buttons_custom_style)}
        <div class="steps-text">Automatically verify the correct formatting of your files, review their contents and
        discuss potential issues.</div>

        {SPB()._html_link_button("Metadata", "?page=metadata", custom_style=buttons_custom_style)}
        <div class="steps-text">Easily edit any metadata relevant to your paper such as authors, keywords, description
        and more.</div>

        {SPB()._html_link_button("Export", "?page=export", custom_style=buttons_custom_style)}
        <div class="steps-text">Once all previous steps are complete, review your work and export it to databases such
        as Zenodo.</div>
    </div>
</center>
        """,
        )

        self.layout.divider()

        from solidipes.utils import get_completed_stages

        complete_stages = get_completed_stages()
        incomplete_stages = [e for e in range(3) if e not in complete_stages]
        incomplete_stages += [3]
        last_stage = min(incomplete_stages)
        steps_names = ["acquisition", "curation", "metadata", "export"]

        SPB(layout=self.layout)._link_button(
            f"Proceed to {steps_names[last_stage]}",
            url=f"?page={steps_names[last_stage]}",
            type="primary",
            use_container_width=True,
        )
