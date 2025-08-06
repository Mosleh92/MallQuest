class ImplementationPlan:
    """Defines phased rollout features for the MallQuest project."""

    def phased_rollout(self):
        """Return a dictionary of project phases and their features."""
        return {
            'phase_1_mvp': {  # أسبوع 1-4
                'duration': '4 weeks',
                'features': [
                    'Basic coin collection',
                    'User registration/login',
                    'Simple quests',
                    'Store check-ins',
                    'Basic leaderboard'
                ]
            },
            'phase_2_social': {  # شهر 2-3
                'duration': '8 weeks',
                'features': [
                    'Team formation',
                    'Chat system',
                    'First gambling game',
                    'Social features',
                    'Push notifications'
                ]
            },
            'phase_3_scale': {  # شهر 4-6
                'duration': '12 weeks',
                'features': [
                    'All 5 gambling games',
                    'AR features',
                    'Voice chat',
                    'Tournament system',
                    'VIP subscriptions'
                ]
            },
            'phase_4_expand': {  # شهر 7-12
                'duration': '24 weeks',
                'features': [
                    'Multi-mall network',
                    'International expansion',
                    'White-label solutions',
                    'Advanced analytics',
                    'AI personalization'
                ]
            }
        }
