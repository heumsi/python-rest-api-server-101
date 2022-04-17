# 파이썬 설치하기

코딩을 하기 위한 언어인 파이썬부터 설치해봅시다.

## pyenv 설치

파이썬 설치 및 버전 관리는 [pyenv](https://github.com/pyenv/pyenv)로 합니다. 
공식 문서에 설치 방법이 잘 나와있습니다. 

여기서는 macOS 기준으로 설명합니다. (다른 OS는 공식 문서를 참고해주세요.)  
macOS에서는 다음처럼 `brew` 로 간단하게 설치할 수 있습니다.

```bash
$ brew update
$ brew install pyenv
```

설치 이후 다음처럼 shell 설정 파일에 `init` 관련 커맨드를 추가해야합니다.  
이를 위해 다음 명령어를 실행해주세요. (zsh shell 기준입니다.) 

```bash 
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

설정 적용을 위해 다음 명령어를 실행해주세요.

```bash
source ~/.zshrc
```

이제 다음처럼 pyenv가 잘 설치되어있는지 확인할 수 있습니다.

```bash
$ pyenv --version

pyenv 2.2.4
```

## Python 설치

설치한 pyenv로 python을 설치해봅시다.

먼저 다음 명령어로 pyenv로 설치할 수 있는 python 버전 목록을 볼 수 있습니다.

```bash
$ pyenv install --list

Available versions:
  2.1.3
  2.2.3
  2.3.7
  2.4.0
  2.4.1
  ...
```

이 중 `3.9.10` 을 설치해봅시다. 다음 명령어를 실행합니다.

```bash
pyenv install 3.9.10
```

설치가 완료되면 다음 명령어로 설치한 파이썬 버전을 확인할 수 있습니다.

```bash
$ pyenv versions

  system
* 3.9.10
```

`3.9.10` 버전을 사용하기 위해 다음 명령어를 실행합니다.

```bash
$ pyenv shell 3.9.10
```

다음 명령어로 현재 설정된 파이썬 버전을 확인할 수 있습니다.

```bash
$ pyenv versions

system
* 3.9.10 (set by PYENV_VERSION environment variable)
```
