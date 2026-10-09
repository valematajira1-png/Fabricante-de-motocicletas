def chart_config(fig):
    fig.update_layout(
        margin=dict(l=20, r=20, t=55, b=20),
        height=330,
        hovermode="x unified",
        legend_title_text="",
    )
    return fig
