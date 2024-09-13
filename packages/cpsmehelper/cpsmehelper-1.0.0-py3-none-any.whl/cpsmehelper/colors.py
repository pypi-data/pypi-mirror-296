def get_colors(format: str = 'hash'):

        if format == 'hash':
    
                custom_colors ={
                        'blue_4'                : '#1D3557',
                        'red'                   : '#E63946',
                        'black'                 : '#323232',
                        'white'                 : '#FAFAFA',
                        'green'                 : '#00b695',
                        'blue_2'                : '#008b9a',
                        'blue_3'                : '#457B9D',
                        'blue_1'                : '#A8DADC',
                        'grey_4'                : '#646464',
                        'grey_1'                : '#E1E1E1',
                        'grey_2'                : '#C8C8C8',
                        'grey_3'                : '#969696',
                        'mint_green'            : '#F1FAEE'
                }

        elif format == 'rgb_dec':
                custom_colors ={
                        'blue_4'                : (29, 53, 87),
                        'red'                   : (230, 57, 70),
                        'black'                 : (50, 50, 50),
                        'white'                 : (250, 250, 250),
                        'green'                 : (0, 182, 149),
                        'blue_2'                : (0, 139, 154),
                        'blue_3'                : (69, 123, 157),
                        'blue_1'                : (168, 218, 220),
                        'grey_4'                : (100, 100, 100),
                        'grey_1'                : (225, 225, 225),
                        'grey_2'                : (200, 200, 200),
                        'grey_3'                : (150, 150, 150),
                        'mint_green'            : (241, 250, 238)
                }

        elif format == 'rgb_perc':
                custom_colors ={
                        'blue_4'                : (11.4, 20.8, 34.1),
                        'red'                   : (90.2, 22.4, 27.5),
                        'black'                 : (19.6, 19.6, 19.6),
                        'white'                 : (98, 98, 98),
                        'green'                 : (0, 71.4, 58.4),
                        'blue_2'                : (0, 54.5, 60.4),
                        'blue_3'                : (27.1, 48.2, 61.6),
                        'blue_1'                : (65.9, 85.5, 86.3),
                        'grey_4'                : (39.2, 39.2, 39.2),
                        'grey_1'                : (88.2, 88.2, 88.2),
                        'grey_2'                : (78.4, 78.4, 78.4),
                        'grey_3'                : (58.8, 58.8, 58.8),
                        'mint_green'            : (94.5, 98, 93.3)
                }

        else:
                allowed_formats = ['hash', 'rgb_dec', 'rgb_perc']
                raise ValueError(f"Invalid format: '{format}'. Allowed formats are: {', '.join(allowed_formats)}")

        return custom_colors