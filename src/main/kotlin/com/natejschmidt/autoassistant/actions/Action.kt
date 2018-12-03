package com.natejschmidt.autoassistant.actions

abstract class Action(val index: Int) {
    abstract fun getType(): ActionType
    abstract fun execute()
}