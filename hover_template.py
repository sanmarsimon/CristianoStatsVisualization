'''
    Provides the template for the hover tooltips.
'''

def get_hover_template(button_clicked):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * Club name
            * Season
            - if the button clicked is 'ranking-btn'
                * Club rank 
            - if the button clicked is 'trophies-btn'
                * The number of trophies won by CR7's team 
                * The list of trophies won by CR7's team

        Args:
            button_clicked: which button is clicked
        Returns:
            The hover template with the elements descibed above
    '''
    if button_clicked == 'ranking-btn':
        hover_template  ='<b>Club:</b> %{customdata[0]}<br>'
        hover_template +='<b>Season:</b> %{x}<br>'
        hover_template +='<b>Rank:</b> %{y}<extra></extra>'
    elif button_clicked == 'trophies-btn':
        hover_template  ='<b>Club:</b> %{customdata[1]}<br>'
        hover_template +='<b>Season:</b> %{x}<br>'
        hover_template +='<b>Number of trophies:</b> %{y}<br>'
        hover_template +='<b>Trophies:</b> %{customdata[0]}<extra></extra>'
        
    return hover_template