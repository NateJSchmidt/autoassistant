package com.natejschmidt.autoassistant.actions

import com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models.RandomMinMaxXYClickModel
import javafx.event.EventHandler
import javafx.scene.Parent
import javafx.scene.control.Button
import javafx.scene.input.KeyEvent
import tornadofx.*
import java.awt.MouseInfo
import java.awt.Robot
import java.awt.event.InputEvent
import kotlin.random.Random

class RandomMinMaxXYClickController(val model: RandomMinMaxXYClickModel) : Action() {

    val myRobot = Robot()

    override fun getType(): ActionType {
        return ActionType.RANDOM_MIN_MAX_X_Y_CLICK
    }

    override fun execute() {
        val origX = MouseInfo.getPointerInfo().location.x
        val origY = MouseInfo.getPointerInfo().location.y

        myRobot.mouseMove(Random.nextInt(model.theXMin, model.theXMax + 1), Random.nextInt(model.theYMin, model.theYMax + 1))
        myRobot.mousePress(InputEvent.BUTTON1_MASK)
        myRobot.mouseRelease(InputEvent.BUTTON1_MASK)
        myRobot.mouseMove(origX, origY)
    }
}

class CreateRandomMinMaxXYClickView : Fragment() {
    //model
    val actionList: MutableList<Action> by param()

    //controller stuff
    private var recordingClicks = false
    private var click1X = -1
    private var click1Y = -1
    private var click2X = -1
    private var click2Y = -1
    private var clickCounter = 0

    //view stuff
    private lateinit var theButton: Button

    private val keyEventHandler = EventHandler<KeyEvent> {
        when (clickCounter) {
            0 -> {
                println("clicked once:  ${it.character}")
                click1X = MouseInfo.getPointerInfo().location.x
                click1Y = MouseInfo.getPointerInfo().location.y
            }
            1 -> {
                println("clicked twice: ${it.character}")
                click2X = MouseInfo.getPointerInfo().location.x
                click2Y = MouseInfo.getPointerInfo().location.y
                theButton.fire()
            }
            else -> println("Oh dear, it didn't get removed")
        }
        clickCounter++
    }


    override val root = form {
        form {
            fieldset("Click form") {
                theButton = button("Click button") {
                    action {
                        if (!recordingClicks) {
                            recordingClicks = true
                            clickCounter = 0
                            primaryStage.addEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)
                            // TODO - figure out how to disable the primary stage...probably need a popup
                            println("hiding primary stage")
//                            primaryStage.hide()
//                            primaryStage.requestFocus()
                            println("primary stage hidden")
                        } else {
                            primaryStage.removeEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)
                            recordingClicks = false

                            //update the model with the new action
                            val index = actionList.size
                            val randomMinMaxXYClickModel = RandomMinMaxXYClickModel(index, click1X, click2X, click1Y, click2Y)
                            actionList.add(RandomMinMaxXYClickController(randomMinMaxXYClickModel))

                            println("unhiding primary stage")
//                            primaryStage.show()
                            println("primary stage unhidden")
                            println("created: $randomMinMaxXYClickModel")
                        }
                    }
                }
            }
        }
    }
}