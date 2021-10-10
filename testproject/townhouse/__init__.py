from otree.api import *
import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'townhouse'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    # randomize to treatments
    for player in subsession.get_players():
        if 'color' in subsession.session.config:
            player.color = subsession.session.config['color']
        else:
            player.color = random.choice(['blue', 'red'])
            print('set player.color to', player.color)



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    color = models.StringField()
    hprice = models.CurrencyField(
        label="Как Вы думаете, сколько стоит этот дом?"
    )
    hprice_a = models.CurrencyField(
        label="Как Вы думаете, сколько стоит этот дом?"
    )
    level = models.IntegerField(
        choices=[
        [1, 'Ниже'],
        [2, 'Ровно такая же'],
        [3, 'Выше'],
    ],
        widget=widgets.RadioSelect,
        label="Как вы считаете, настоящая цена дома выше или ниже этого значения?"
    )





# PAGES
class Survey1(Page):
    form_model = 'player'
    form_fields = ['hprice']


    @staticmethod
    def is_displayed(player: Player):
        return player.color == 'red'


# def previous(player: Player):
    # return player.get_others_in_subsession


class Survey2(Page):
    form_model = 'player'
    form_fields = ['level', 'hprice_a']

    @staticmethod
    def is_displayed(player: Player):
        return player.color == 'blue'

    @staticmethod
    def vars_for_template(player: Player):
        target = 100000000
        id = player.id_in_group
        others = player.get_others_in_subsession()
        for person in others:
            if person.id_in_group < id:
                if person.color == 'blue':
                    if person.hprice_a is not None:
                        target = person.hprice_a
        # target = player.get_others_in_subsession
        target = format(int(target), ',').replace(',', ' ').replace('.', ',')
        return dict(
            target=target
        )


class Thanks(Page):
    pass



page_sequence = [Survey1, Survey2, Thanks]
