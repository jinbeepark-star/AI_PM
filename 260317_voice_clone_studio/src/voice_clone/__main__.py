import argparse
import json

from .synthesizer import TtsSynthesizer
from .cloner import VoiceCloner
from .dubbing import DubbingPipeline


def cmd_synthesize(args: argparse.Namespace) -> None:
    synth = TtsSynthesizer()
    result = synth.synthesize(args.text, voice_id=args.voice_id, speed=args.speed)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_clone(args: argparse.Namespace) -> None:
    cloner = VoiceCloner()
    profile = cloner.create_profile(args.sample, args.name)
    print(json.dumps(profile, ensure_ascii=False, indent=2))


def cmd_dub(args: argparse.Namespace) -> None:
    pipeline = DubbingPipeline()
    lines = args.lines.split("|")
    results = pipeline.dub(lines, profile_id=args.profile_id)
    print(json.dumps(results, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice_clone",
        description="Voice Clone Studio CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_synth = sub.add_parser("synthesize", help="텍스트를 음성 메타데이터로 변환")
    p_synth.add_argument("text")
    p_synth.add_argument("--voice-id", default="default")
    p_synth.add_argument("--speed", type=float, default=1.0)
    p_synth.set_defaults(func=cmd_synthesize)

    p_clone = sub.add_parser("clone", help="음성 샘플로 프로필 생성")
    p_clone.add_argument("sample", help="샘플 파일 경로")
    p_clone.add_argument("--name", default="unnamed")
    p_clone.set_defaults(func=cmd_clone)

    p_dub = sub.add_parser("dub", help="스크립트 더빙")
    p_dub.add_argument("lines", help="파이프(|)로 구분된 스크립트 라인")
    p_dub.add_argument("--profile-id", required=True)
    p_dub.set_defaults(func=cmd_dub)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
