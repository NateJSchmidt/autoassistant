package com.natejschmidt.autoassistant.actions

abstract class Action() {
    abstract fun getType(): ActionType
    abstract fun execute()
}