package com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models

import com.fasterxml.jackson.annotation.JsonTypeInfo

@JsonTypeInfo(use = JsonTypeInfo.Id.CLASS, include = JsonTypeInfo.As.PROPERTY, property = "@class")
data class RandomMinMaxXYClickModel(
        override val index: Int = -1,
        val theXMin: Int = -1,
        val theXMax: Int = -1,
        val theYMin: Int = -1,
        val theYMax: Int = -1)
    : ActionModel(index)