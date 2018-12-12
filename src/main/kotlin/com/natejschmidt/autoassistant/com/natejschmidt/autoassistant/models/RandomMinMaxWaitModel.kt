package com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models

import com.fasterxml.jackson.annotation.JsonTypeInfo

@JsonTypeInfo(use = JsonTypeInfo.Id.CLASS, include = JsonTypeInfo.As.PROPERTY, property = "@class")
data class RandomMinMaxWaitModel(
        override val index: Int = -1,
        val minWaitTime: Int = -1,
        val maxWaitTime: Int = -1)
    : ActionModel(index)