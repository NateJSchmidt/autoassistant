package com.natejschmidt.autoassistant.actions

import java.awt.MouseInfo
import java.awt.Robot
import java.awt.event.InputEvent
import kotlin.random.Random

class RandomMinMaxXYClick(index: Int, val xMin: Int, val xMax: Int, val yMin: Int, val yMax: Int) : Action(index) {

    val myRobot = Robot()

    override fun getType(): ActionType {
        return ActionType.RANDOM_MIN_MAX_X_Y_CLICK
    }

    override fun execute() {
        val origX = MouseInfo.getPointerInfo().location.x
        val origY = MouseInfo.getPointerInfo().location.y

        myRobot.mouseMove(Random.nextInt(xMin, xMax+1), Random.nextInt(yMin, yMax+1))
        myRobot.mousePress(InputEvent.BUTTON1_MASK)
        myRobot.mouseRelease(InputEvent.BUTTON1_MASK)
        myRobot.mouseMove(origX, origY)
    }
}