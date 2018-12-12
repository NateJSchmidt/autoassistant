package com.natejschmidt.autoassistant.actions

import com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models.RandomMinMaxWaitModel
import javafx.beans.property.SimpleIntegerProperty
import tornadofx.*
import kotlin.random.Random

class RandomMinMaxWaitController(val model: RandomMinMaxWaitModel) : Action() {
    override fun getType(): ActionType {
        return ActionType.RANDOM_MIN_MAX_WAIT
    }

    override fun execute() {
        Thread.sleep(1000L * Random.nextInt(model.minWaitTime, model.maxWaitTime+1).toLong())
    }

}

class CreateRandomMinMaxWaitView : Fragment() {
    // model
    val actionList: MutableList<Action> by param()

    private val minWaitTime = SimpleIntegerProperty()
    private val maxWaitTime = SimpleIntegerProperty()

    override fun onDock() {
        super.onDock()
        resetToInitialValues()
    }

    private fun resetToInitialValues() {
        minWaitTime.value = 0
        maxWaitTime.value = 1
    }

    override val root = form {
        fieldset("Wait Times") {
            field("Minimum wait time (seconds)") {
                textfield {
                    filterInput {
                        it.controlNewText.isInt()
                    }
                }.bind(minWaitTime)
            }
            field("Maximum wait time (seconds)") {
                textfield {
                    filterInput {
                        it.controlNewText.isInt()
                    }
                }.bind(maxWaitTime)
            }
        }
        button("Create action") {
            action {
                println("Creating randomized wait time action")
                val index = actionList.size
                actionList.add(RandomMinMaxWaitController(
                        RandomMinMaxWaitModel(index, minWaitTime.value, maxWaitTime.value)))
                resetToInitialValues()
            }
        }
    }
}