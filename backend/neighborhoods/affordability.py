def calculate_real_affordability(rent_data, income=None):
    """
    Calculates REAL affordability based on
    NYC median income and the 30% rule.

    The 30% Rule:
    You should spend no more than 30%
    of your monthly income on rent.

    NYC Median Income: $70,000/year
    Monthly: $5,833/month
    30% of monthly: $1,750/month recommended max

    Returns detailed affordability breakdown
    """

    # NYC median household income 2026
    NYC_MEDIAN_INCOME_YEARLY = 70000
    NYC_MEDIAN_INCOME_MONTHLY = NYC_MEDIAN_INCOME_YEARLY / 12

    # Use provided income or NYC median
    if income:
        monthly_income = income / 12
    else:
        monthly_income = NYC_MEDIAN_INCOME_MONTHLY

    # 30% rule recommended max rent
    recommended_max = monthly_income * 0.30
    comfortable_max = monthly_income * 0.25
    stretching_max = monthly_income * 0.40

    try:
        studio = rent_data.studio
        one_br = rent_data.one_bedroom
        two_br = rent_data.two_bedroom
        three_br = rent_data.three_bedroom or 0

        def get_rating(rent):
            """
            Rates affordability of a unit
            based on income and 30% rule
            """
            rent_ratio = rent / monthly_income

            if rent <= comfortable_max:
                return {
                    'rating': 'Very Affordable',
                    'icon': '✅',
                    'color': '#16A34A',
                    'percentage': round(rent_ratio * 100, 1),
                    'monthly_remaining': round(
                        monthly_income - rent, 0
                    )
                }
            elif rent <= recommended_max:
                return {
                    'rating': 'Affordable',
                    'icon': '👍',
                    'color': '#65A30D',
                    'percentage': round(rent_ratio * 100, 1),
                    'monthly_remaining': round(
                        monthly_income - rent, 0
                    )
                }
            elif rent <= stretching_max:
                return {
                    'rating': 'Stretching Budget',
                    'icon': '⚠️',
                    'color': '#D97706',
                    'percentage': round(rent_ratio * 100, 1),
                    'monthly_remaining': round(
                        monthly_income - rent, 0
                    )
                }
            else:
                return {
                    'rating': 'Not Affordable',
                    'icon': '❌',
                    'color': '#DC2626',
                    'percentage': round(rent_ratio * 100, 1),
                    'monthly_remaining': round(
                        monthly_income - rent, 0
                    )
                }

        return {
            'income_used': {
                'yearly': round(monthly_income * 12, 0),
                'monthly': round(monthly_income, 0),
                'source': 'Provided' if income else 'NYC Median'
            },
            'recommended_max_rent': round(recommended_max, 0),
            'comfortable_max_rent': round(comfortable_max, 0),
            'stretching_max_rent': round(stretching_max, 0),
            'units': {
                'studio': {
                    'rent': studio,
                    **get_rating(studio)
                },
                'one_bedroom': {
                    'rent': one_br,
                    **get_rating(one_br)
                },
                'two_bedroom': {
                    'rent': two_br,
                    **get_rating(two_br)
                },
                'three_bedroom': {
                    'rent': three_br,
                    **get_rating(three_br)
                } if three_br else None
            },
            'summary': get_overall_summary(
                studio, one_br, recommended_max
            )
        }

    except Exception as e:
        return {'error': str(e)}


def get_overall_summary(studio, one_br, recommended_max):
    """
    Returns overall affordability summary
    for the neighborhood
    """
    if studio <= recommended_max:
        return {
            'verdict': 'Affordable for median income earners',
            'icon': '✅',
            'color': '#16A34A',
            'tip': f'Studio at ${studio}/mo fits within '
                   f'the recommended ${recommended_max:.0f}/mo budget'
        }
    elif one_br <= recommended_max * 1.2:
        return {
            'verdict': 'Slightly above median budget',
            'icon': '⚠️',
            'color': '#D97706',
            'tip': f'Consider roommates or a studio '
                   f'to stay within budget'
        }
    else:
        return {
            'verdict': 'Above median income budget',
            'icon': '❌',
            'color': '#DC2626',
            'tip': f'This neighborhood requires above '
                   f'average income or roommates'
        }