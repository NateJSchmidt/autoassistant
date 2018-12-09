package com.natejschmidt.autoassistant.main

import com.fasterxml.jackson.databind.ObjectMapper
import com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models.RandomMinMaxXYClickModel

fun main(args: Array<String>) {
    val randomMinMaxXYClickModel = RandomMinMaxXYClickModel(3, 5, 10, 15, 20)

    val OM = ObjectMapper()

    val json = OM.writeValueAsString(randomMinMaxXYClickModel)
    println(json)
    println()
    val result = OM.readValue(json, RandomMinMaxXYClickModel::class.java)
    println(result)
}