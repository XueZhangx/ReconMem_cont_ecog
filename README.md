The task is to respond 0 to images that the subject didn't see and 1 to images that the subject has seen. 

To run practice, run the following. $subid can go from 1-50. Let's start from subject 2. 
```
cd ./Scripts/Presentation
# python practice_block.py $subID
python practice_block.py 2
```

This will give a practice of 20 trials with feedback. There won't be any feedback in the actual experiment. 
To run the actual study, 

```
cd ./Scripts/Presentation
# python run_exp_block $subID $blockID
python run_exp_block.py 2 1 
```
$blockID can go from 1 to 11. Each block lasts about 6.25 mins so we can probably only cover about 7 blocks in a 45-min session. 
