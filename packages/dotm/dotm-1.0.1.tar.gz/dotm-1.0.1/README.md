# dotm

dotm: **D**otfiles **O**rganized, **T**racked, and **M**anaged.

dotm is my take on $HOME and `.config` directory backup solutions. Originally authored in March 15, 2022 with [this commit](https://github.com/fybx/scripts/commit/0b4f6f32e1b94603a0ae549ec3342ce79a5b81a7), dotm now is a stable and well-thought solution.

## features

- [x] backup/deploy to/from a remote repository
- [ ] add comments to backups
- [ ] create tags with backups & deploy tags
- [ ] track deletions (in a seperate commit)

### technical features

- [ ] use LUT to improve backup/deploy times if `deploy_list` is not changed
- [ ] message and log at the same time
- [ ] provide AUR package

## how to use?

1. acquire dotm
2. `dotm init --local -u https://example.org/~user/dotfiles`
3. create whitelist `deploy_list` at `.config/dotm/deploy_list`
4. `dotm backup`

Congrats! You've successfully committed your configuration.

For a detailed walkthrough, see [docs/usecases.md](docs/usecases.md).

## credits

Feel free to contact me for collaboration on anything!

Yiğid BALABAN, <[fyb@fybx.dev][llmail]>

[My Website][llwebsite] • [My Bento][llbento] • [X][llx] • [LinkedIn][lllinkedin]

2024

[llmail]: mailto:fyb@fybx.dev
[llwebsite]: https://fybx.dev
[llbento]: https://bento.me/balaban
[llx]: https://x.com/fybalaban
[lllinkedin]: https://linkedin.com/in/fybx

