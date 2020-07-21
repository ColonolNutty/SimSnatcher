This page is a reference for the various interactions added by Sim Snatcher.

**For all interactions that require SHIFT + CLICK (SHIFT + CLICK? is Yes), you need to enable Testing Cheats by putting this command in the CTRL + SHIFT + C console "testingcheats on" before they will appear**

# Abduction:

## Main:
| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Attempt To Abduct | Sim | Sim Snatcher -> Abduction | When chosen, your Sim will attempt to capture the Target Sim. | No | Yes |
| Release Captive | Sim | Sim Snatcher -> Abduction | When chosen, your Sim will release the Target Sim and they will no longer be a Captive. | No | Yes |

## Debug Interactions:
These are interactions mainly used for debugging purposes or to fix things that break.

| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Clear Abduction Data | Sim | Sim Snatcher -> Abduction | When chosen, the Target Sim will be cleaned of all abduction data, they will be released, and if they are a Captor, any Captives they have will be released as well. | Yes | No |
| Force Abduct | Sim | Sim Snatcher -> Slavery | When chosen, the Target Sim will become a Captive to the Active Sim. | Yes | No |

# Slavery:
- In order to create a Slave, your Sim must first successfully Abduct them, see [Abduction Interactions](#abduction).
## Main:
| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Attempt To Enslave | Sim | Sim Snatcher -> Slavery | When chosen, your Sim will attempt to enslave the Target Abducted Sim. | No | Yes |
| Release Slave | Sim | Sim Snatcher -> Slavery | When chosen, your Sim will release the Target Slave Sim and they will no longer be a Slave. | No | Yes |

## Slave Interactions:
| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Enable Cleaning Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will start performing Cleaning tasks. | No | Yes |
| Disable Cleaning Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will stop performing Cleaning tasks. | No | Yes |
| Enable Repair Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will start performing Repair tasks. | No | Yes |
| Disable Repair Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will stop performing Repair tasks. | No | Yes |
| Enable Gardening Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will start performing Gardening tasks. | No | Yes |
| Disable Gardening Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will stop performing Gardening tasks. | No | Yes |
| Enable Childcare Tasks | Slave Sim | Slave -> Tasks | When chosen, the Slave will start performing Childcare tasks. | No | Yes |
| Disable Childcare Tasks | Slave Sim | Slave -> Tasks | When selected, the Slave will stop performing Childcare tasks. | No | Yes |
| Dismiss All Visitors | Slave Sim| Slave -> Greeting | When selected, the Slave will send all visiting Sims home. | No | Yes |
| Invite All Visitors Inside | Slave Sim | Slave -> Greeting | When chosen, the Slave will invite all visiting Sims into the home. | No | Yes |
| Ignore Front Door | Slave Sim| Slave -> Greeting | When selected, the Slave will ignore any visitors that knock on the front door. | No | Yes |
| Praise | Slave Sim| Slave -> Management | When chosen, your Active Sim will praise the Slave. | No | Yes |
| Reprimand | Slave Sim| Slave -> Management | When chosen, your Active Sim will reprimand the Slave. | No | Yes |
| Repair An Object | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to repair a random broken object on the lot. | No | Yes |
| Go To Sleep | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to go to sleep. | No | Yes |
| Clean a Dirty Object | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to clean dirty objects. | No | Yes |
| Check On Children | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to check on the children and ensure their needs are being met. | No | Yes |
| Cook Meal | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to make a meal with a Single Serving. | No | Yes |
| Cook Family Meal | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to make a meal with a enough servings for a Family (Vanilla is 4). | No | Yes |
| Cook Party Meal | Slave Sim | Slave -> Orders | When chosen, your Active Sim will order the Slave to make a meal with a enough servings for a Party (Vanilla is 8). | No | Yes |
| Burn Up the Dance Floor| Slave Sim | Slave -> Orders | Order the Slave to dance on a Dance Floor. | No | Yes |
| Perform Comedy Routine | Slave Sim | Slave -> Orders | Order the Slave to perform a comedy routine on a Microphone. | No | Yes |
| Play Guitar | Slave Sim | Slave -> Orders | Order the Slave to play the Guitar. | No | Yes |
| Play Piano | Slave Sim | Slave -> Orders | Order the Slave to play the Piano. | No | Yes |
| Play Violin | Slave Sim | Slave -> Orders | Order the Slave to play the Violin. | No | Yes |
| Use DJ Booth | Slave Sim | Slave -> Orders | Order the Slave to DJ at a DJ Booth. | No | Yes |
| Water Plants | Slave Sim | Slave -> Orders | Order the Slave to water plants that need watering. | No | Yes |
| Prepare Bar Drink | Slave Sim | Slave -> Orders | Order the Slave to prepare drinks at a Bar. | No | Yes |

## Debug Interactions:
- These are interactions mainly used for debugging purposes or to fix things that break.

| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Clear Slavery Data | Sim | Sim Snatcher -> Slavery | When chosen, the Target Sim will be cleaned of all slavery data, they will be released, and if they are a Master, any Slaves they have will be released as well. | Yes | No |
| Force Enslave | Sim | Sim Snatcher -> Slavery | When chosen, the Target Sim will become a Slave to the Active Sim. | Yes | No |

# Orders:

- A Sim must be a Captive or a Slave to order them around.

| Interaction Name | Interaction Location | Interaction Path | What It Does | SHIFT + CLICK? | CLICK? |
| ---------------- | -------------------- | ---------------- | ------------ | -------------- | ------ |
| Go Here | Terrain | Sim Snatcher -> Order To | When chosen, your Sim will order the selected Sim to go to the target location. | No | Yes |
| Perform Interaction | Sim, Object, Terrain | Sim Snatcher -> Order To | When chosen, your Sim will order the selected Sim to perform the selected interaction at or with the target location, Sim, or object. _(Not every interaction will successfully execute!)_ | No | Yes |
| Go To Residence | Sim | Sim Snatcher -> Order To | When chosen, your Sim will order the Target Sim to go to the Home Lot of your Sim and your Sim will travel there with them. | No | Yes |