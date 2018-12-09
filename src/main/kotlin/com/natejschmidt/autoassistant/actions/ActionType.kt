package com.natejschmidt.autoassistant.actions

enum class ActionType {
    RANDOM_MIN_MAX_WAIT{
        override fun toString(): String {
            return "Random timed wait"
        }
    },
    RANDOM_MIN_MAX_X_Y_CLICK {
        override fun toString(): String {
            return "Random X,Y click"
        }
    }
}