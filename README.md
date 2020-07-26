## Kniffel / Yahtzee

This is a game which makes the populare game Kniffel playable on your computer using python with pygame.

## What is Kniffel?
Kniffel or also known as Yahtzee is a popular game. The goal of the game is to roll different combinations with five dices.
For example if you would roll this combination...

<img width="40%" style="display:block;margin-left:auto;margin-right:auto;" src="https://raw.githubusercontent.com/sp4c38/kniffel/master/readme_assets/example_dice_roll.png">

... you would count all threes together which would be 9 and register the reached points in a table like this:

<img width="50%" style="display: block; margin-left:auto; margin-right:auto;" src="https://raw.githubusercontent.com/sp4c38/kniffel/master/readme_assets/kniffel_table.png">

So you could register 9 in the "Threes" column. You also could register them in "Three Of A Kind". 

There are multiple different combinations which you have to reach to win the game.

For futher explanation see [this Wikipedia article.](https://en.wikipedia.org/wiki/Yahtzee)

## Prerequisites
Right now the latest pygame version is 1.9.6 which was released on April 25, 2019. This game uses the pygame version 2.0.0.dev10 which is a pre-release because this release fixes some issues in 1.9.6 and supports python3.8.

- pygame version 2.0.0.dev10
- works on python3.7 and python3.8 (not tested on other versions)