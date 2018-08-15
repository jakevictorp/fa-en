# fa-en

The taggers in this repository are based on scripts from the Hazm toolkit (https://github.com/sobhe/hazm) and use the pre-trained model included in the toolkit.

The transliterator is a one-to-one Perso-Arabic to Latin transliterator. It is a modified version of a transliterator for Arabic using the Buckwalter system. The original script can be found at: https://www.redhat.com/archives/fedora-extras-commits/2007-June/msg03617.html

I have also provided a script to "shrink" training corpora in order to simulate a low-resource setting. The shrunken corpus will always be composed of sentences extracted from the original corpus at even intervals to ensure that all parts of the original corpus are evenly represented. The script allows the user to specify the desired fraction of the original corpus.
