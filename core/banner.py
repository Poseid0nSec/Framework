import textwrap
from core import config


def banner():
    print(textwrap.dedent(f"""
                 _nnnn_
                dGGGGMMb
               @p~qp~~qMb
               M|@||@) M|
               @,----.JM|
              JS^\\__/  qKL
             dZP        qKRb
            dZP          qKKb                       Pentest Framework v{config.version}
           fZP            SMMb           Github: https://github.com/Poseid0nSec/Framework
           HZM            MMMM
           FqM            MMMM
         __| ".        |\\dS"qML
         |    `.       | `' \\Zq
        _)      \\.___.,|     .'
        \\____   )MMMMMP|   .'
             `-'       `--' hjm
    """))
