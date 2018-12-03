package com.natejschmidt.autoassistant.actions

enum class ActionType(val strVal: String) {
    RANDOM_MIN_MAX_WAIT("Random timed wait"),
    RANDOM_MIN_MAX_X_Y_CLICK("Random X,Y click")
}

fun main(args: Array<String>) {
    val strings = mutableListOf<String>()
    ActionType.values().forEach { strings.add(it.strVal) }
    println(strings)
}