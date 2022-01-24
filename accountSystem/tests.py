from django.test import TestCase

# Create your tests here.
if __name__ == '__main__':
    y = 'abcdefg'.split('cd')
    print(y)
    x = ':'.join(y)
    print(x)