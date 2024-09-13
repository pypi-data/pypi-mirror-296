"""Reflex custom component for React east-react-text-loop"""

from typing import Literal
import reflex as rx

LiteralAnimationTypes = Literal["tween", "spring", "inertia", "keyframes", "just"]


class TextLoop(rx.Component):
    library = "easy-react-text-loop"

    tag = "TextLoop"

    is_default = False

    # Props
    #

    timeout: int = 2500

    animation: rx.Var[LiteralAnimationTypes] = "tween"


TextLoop = TextLoop.create
