# mesh2stress
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

![Icon](src/icon.png)
>  Calculate stress based on the mesh before and after deformation.

---

## Version
- v0.1.0
> This is currently a work in progress. Will take some time to finish writing the code over the next few months.

## Language
- [中文]

## License
- MIT

## Description
The program extracts the displacement field based on the source mesh and the target mesh before and after deformation, and calculates the stress distribution. The code was written in <b>python</b> primarily to be easy to read and rapid development, so it did not play with full computational efficiency. A later version (V2) is planned to optimize the core code by using C++.

![the source mesh and the target mesh](./src/mesh.png)

![process](./src/process.png)


[中文]: /documents/README.zh-CN.md