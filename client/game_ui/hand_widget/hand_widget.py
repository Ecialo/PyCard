# -*- coding: utf-8 -*-
__author__ = 'ecialo'

import kivy
import kivy.uix.floatlayout as flayout
import kivy.uix.anchorlayout as alayout
import kivy.uix.relativelayout as rlayout
import kivy.uix.stacklayout as slayout
import kivy.uix.boxlayout as blayout
import kivy.uix.widget as widget
import kivy.uix.label as label
import kivy.uix.button as button
import kivy.properties as prop

from kivy.lang import Builder

from core import predef

Builder.load_file('./client/game_ui/hand_widget/hand_widget.kv')

class HandWidget(blayout.BoxLayout):

    hand = prop.ObjectProperty()

    game_widget = prop.ObjectProperty()

    game_widget = prop.ObjectProperty()
    player_widget = prop.ObjectProperty()

    def __init__(self, hand, **kwargs):
        super(HandWidget, self).__init__(**kwargs)
        self.hand = hand

        self.register_event_type('on_get_cards')

    def on_get_cards(self, cards):
        for card in cards:
            card = self.game_widget.game.view_card(card)

            card_widget = card.make_widget(game_widget=self.game_widget)
            is_our_hand = (self.game_widget.player_name == self.player_widget.player.name)
            card_widget.origin = predef.CARD_FROM_OUR_HAND if is_our_hand else predef.CARD_FROM_ANOTHER_HAND
            self.ui_add_card_widget(card_widget)

    def try_to_get_card(self, card_widget, touch_pos):
        if card_widget.origin == predef.CARD_FROM_OUR_HAND:
            self.ui_add_card_widget(card_widget, touch_pos)

        # пытаемся взять карту из колоды, если можно
        elif card_widget.origin == predef.CARD_FROM_DECK:
            if self.game_widget.is_our_turn() and self.game_widget.is_our_tab_active():
                #TODO: это выглядит неправильно.
                g = self.game_widget.game
                atable = g.get_category(predef.TABLE)['game_action_table']
                dca_class = filter(lambda x: x.name == 'draw_cards', atable.actions)[0]
                draw_card = dca_class(
                        source=self.game_widget.deck_widget.deck,
                        target=self.hand,
                        number=1,
                        author=self.game_widget.player_name)

                if draw_card.check():
                    self.game_widget.send_actions(draw_card)

                card_widget.origin = predef.CARD_FROM_OUR_HAND
            elif not self.game_widget.is_our_turn():
                self.game_widget.notify("It's not your turn now")

        card_widget.size_hint_y = 1

    def ui_add_card_widget(self, card, touch_pos=None):
        if touch_pos:
            for i, c in enumerate(self.ids.card_stack.children):
                if c.collide_point(*touch_pos):
                    self.ids.card_stack.add_widget(card, i)
                    return

        self.ids.card_stack.add_widget(card)

