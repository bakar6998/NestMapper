def detect_trend(neighborhood):
    """
    Detects if a neighborhood is
    Rising, Stable or Declining
    based on its scores

    Returns trend info with icon
    and description
    """
    try:
        scores = neighborhood.scores

        overall = scores.overall_score
        safety = scores.safety_score
        affordability = scores.affordability_score
        transit = scores.transit_score

        # Determine trend based on scores
        if overall >= 8.0:
            trend = "Rising"
            icon = "📈"
            color = "#16A34A"
            description = (
                f"{neighborhood.name} is a highly rated "
                f"neighborhood with excellent overall scores. "
                f"Strong demand and quality of life."
            )
        elif overall >= 6.5:
            if safety >= 7.0 and affordability >= 7.0:
                trend = "Rising"
                icon = "📈"
                color = "#16A34A"
                description = (
                    f"{neighborhood.name} shows positive "
                    f"indicators with good safety and "
                    f"affordability scores."
                )
            elif safety < 5.0:
                trend = "Declining"
                icon = "📉"
                color = "#DC2626"
                description = (
                    f"{neighborhood.name} faces challenges "
                    f"with below average safety scores "
                    f"affecting overall desirability."
                )
            else:
                trend = "Stable"
                icon = "➡️"
                color = "#D97706"
                description = (
                    f"{neighborhood.name} is a stable "
                    f"neighborhood with consistent "
                    f"scores across all dimensions."
                )
        elif overall >= 5.0:
            if affordability >= 8.0:
                trend = "Rising"
                icon = "📈"
                color = "#16A34A"
                description = (
                    f"{neighborhood.name} is an affordable "
                    f"area showing signs of improvement "
                    f"and growing interest."
                )
            else:
                trend = "Stable"
                icon = "➡️"
                color = "#D97706"
                description = (
                    f"{neighborhood.name} maintains "
                    f"steady performance with room "
                    f"for improvement."
                )
        else:
            trend = "Declining"
            icon = "📉"
            color = "#DC2626"
            description = (
                f"{neighborhood.name} shows below "
                f"average scores across multiple "
                f"dimensions requiring attention."
            )

        return {
            'trend': trend,
            'icon': icon,
            'color': color,
            'description': description,
            'scores': {
                'overall': overall,
                'safety': safety,
                'affordability': affordability,
                'transit': transit
            }
        }

    except Exception as e:
        return {
            'trend': 'Unknown',
            'icon': '❓',
            'color': '#9CA3AF',
            'description': 'Unable to determine trend',
            'scores': {}
        }


def detect_all_trends():
    """
    Detects trends for ALL neighborhoods
    Returns summary of rising, stable
    and declining areas
    """
    from .models import Neighborhood

    neighborhoods = Neighborhood.objects.all()

    rising = []
    stable = []
    declining = []

    for n in neighborhoods:
        trend_data = detect_trend(n)
        trend_data['neighborhood'] = n.name
        trend_data['borough'] = n.borough

        if trend_data['trend'] == 'Rising':
            rising.append(trend_data)
        elif trend_data['trend'] == 'Stable':
            stable.append(trend_data)
        else:
            declining.append(trend_data)

    return {
        'rising': rising,
        'stable': stable,
        'declining': declining,
        'summary': {
            'total': len(neighborhoods),
            'rising_count': len(rising),
            'stable_count': len(stable),
            'declining_count': len(declining)
        }
    }