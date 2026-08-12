"""
Wall Envy - Asset Downloader
Downloads all images from the Google Sites website and saves them locally.
Run this script once from the repo root: python scripts/download-assets.py
"""

import os
import re
import time
import urllib.request
from urllib.error import URLError, HTTPError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PROJECTS_DIR = os.path.join(IMAGES_DIR, "projects")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download(url, dest_path, label=""):
    if os.path.exists(dest_path):
        print(f"  [skip] {label or os.path.basename(dest_path)} (already exists)")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(data)
        print(f"  [ok] {label or os.path.basename(dest_path)} ({len(data)//1024}KB)")
        return True
    except (URLError, HTTPError, Exception) as e:
        print(f"  [fail] {label or os.path.basename(dest_path)}: {e}")
        return False

# ============================================================
# Brand / UI images
# ============================================================
BRAND_IMAGES = {
    # Hero banner - WALL ENVY rainbow logo with paint splash
    "hero-banner.png": "https://lh3.googleusercontent.com/sitesv/AG8ngQVs1buBqtMNmPFeYtSovWyDge5ORDB1_IgPoQw9U3BF71fkKQkn9TuOWaVUBEoG3UgHEQwxkd7TgH58uW8zeHq9CCevkptODmUUamPZyIP1P7j5f3HZ5nok_246fbXHlvQi6VZ0TVZL7NJ7lPMZEhPZR2-OzYaJD1TaL0P9EsKxjxM16gmb939T2gDrTMONYkRJtlb_uiDR-LK6PHsiiHH81lZOV=w1280",
    # CTA banner (used in footer CTA strip on all pages)
    "cta-banner.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXOm9-wAzJXyrwIODWZPB9aeghaEkgp4UdX5cYfkThIRPYqRFD5K2YwdEoOAyuYafyCEbLjjuWA9bpdDTSuN6eCDrBRVjID5G-IbhqWPBmqFsLfAYFTfso-GlEJGVgSvUOmGJj_k_ngJV9-jF2Kx--cqWG3aAFCYgX1qBZ2b-Lgr41Z3Mx5vYskQpVOEnKJhciMfab7ENCYpI7TijqjO-3cPi-rOketXFcVnmh18HY=w1280",
    # Secondary hero image (home page)
    "hero-wall.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQU-nmnLmhGVCpCop1tEk7JqhFiD2AeZZ7VDpah1E_g_wNffxq_OlBRFSWIG3JJArfxaAuV17udwzoxjhObIJi2243AErw1Q5exldZqHjIXZs6xBwhJu298ru6CxIutw9bRsRViGzTzjypyXqhz9WseBZDbEMzX985y_2Y3YRStWjEoX93Sc2VbMIHvqLLL77DP45nqPBk7yD6aXKqDN2OgTuX1pXbGSpgScQA3r=w1280",
    # FAQ / Why Choose Us banner
    "faq-banner.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXDY__M6We0so16RyCUt5YRshm08iHnYmdf89U7YTKbBqOkmBwGz_Yvk0lCEIwaNiLxH4TgDkxK-bvBw1UXsTk390byxsRBEx9H_WkKzop1CFbCJS2wO3Ro2b0NYb5UAoNpcn9XxhttZWMkuIck8SR4zTMTPg_L-kF396kMfdTwwTq5VswJBmET6LQJn_KgPXl9sJ7Adb18av7m-_kgVTwHUAqyYlOo__UYS-xBtLg=w1280",
}

# ============================================================
# Project gallery images (from Projects page)
# ============================================================
PROJECT_IMAGES = {
    "proj-01.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQWEoZkyIOU9jdG6PYa-rSGn81q_KnqbXe9LFSWz9mnPFM4b093o0F5AvfmiGIKtLDA2rNGmjl5llRPdzi4f7atQXmugnG1WOzQkNanTnrg2GZQxDded3daEmDPLYCnxiSUI9z0aXB_m3362FF4zXJOUKhBHq9c1HnjQBywk8IXbBf_rDHUEnvkJHMzny-D0cQaMYjJWyISfiSQN_goZpH_sQl3dRP=w1280",
    "proj-02.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXwR1DPOynZGFdHZiVpDyiYzNinucIi_SFto7_f5AICmzA5JkNaiizJfsD4VCmHyO2bILWoLX54aoig61vvUg2pTWawfL2Eja_gAtlV3HNwsN4MDy9TVIe1dk68YVGpOwmfpzrsRexTizH0fw9yBulLrtls8ZZqZxtfwpLNmxnV0v49EpHfFH_9YOuSHoHsjksPEoTf6qa1LhBuqjkr2pkd608eQd6LPCkmTbYb-VE=w1280",
    "proj-03.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQVVvem99SUmagNRm31dUcSuJbTl4RLI29kgmH59eAtfwQzK7s8e3-8EZqQcjXrOClIM45mXQAMWXiUW_6w0RcjasAniohS5jk7U_KI4LPidXPHT09RpCEbouZF62Q45dWGsr6AmtOmV3WDufJRQgLu8XqmnHBf_tu6YY7PMREYp1FcNASwHWlszF4StpBrChqkEcRL0FVeLlk-nPRBwFCqCoTf9cR0BXKvyl7nvVOc=w1280",
    "proj-04.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXlceXm58YZHGO5gd7G83VaVCGmrb8raX05LN9wm-Z5mDwNZmiG77Mu-bJA1QAPWLqO-IsbrmtHpb-MD68qBL9etj676aCTpxjUV1quPs_FIdCA2R17--0jVKLvKOp9VRu513NoS-zAlKMmQQEtk9HqFCnBkQcR7fkWQ1MT3JS8xDd5OaQzu6HOyMPATd0dGBmDi1dBMBwNPbh57_b8H0LVjIZYrrkdu_LCVTQ=w1280",
    "proj-05.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQWXyxn6kOOJgJ0xD2vVx89yUzTpF8y3gj9LjfbU24JXNZss0tm8NCdFnowdgkf-Y8KdlztWvVyDHIzSfw5WJOhIpO42cfBUf9k8aHkhtbFlqFtf0VJbaWrrSJzinU062L9J1HYJpnQZ5dWuZq6Dvhxiy7OICTX4SlDBlP_2XQqCoUyewqzh-B9kFYO2=w1280",
    "proj-06.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQU7IjbvZ15R6OmEwRo7nsALSimggS5NUhbLXNNENd_HME8fCMe8LNMfCFJvHeKGY-gk39NZgYLd78ddrFq3I9eYgDOahK0CBTs_ffLv9sZHmqpX6iw57Ns1DltfG8O_M1_jfqkRbxKYTE7Ui1LFB_79JSKGnTAEDItjwrmBp5CMXDJrzGt_SZEyiTb9=w1280",
    "proj-07.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXlUUHe_1bMUwamJJCbkBWmrd_PEwvF3pdxLa3zquwAjHqqme7vJ-kD8tXpjP8OwGdZeoJO8NgXofHgWBD_JgSCxBIZqpMstE95thVgzeXGbCwYqx_2PIZWcv_6iKKiEt_1QAeGJmHeFWAX9qkB3Jep3QWY6CX5G3nC0i6xR0_J10Do4-x3sIFC-fzXfvdMrkqZSlZS5yaMzMObeHUbsyF47yvCE2u9GYSsh-Y2k=w1280",
    "proj-08.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXQf8sdLacnIsxeeonQA5GMmz1KGul6zw4ItHeh9lIkgw5Nzd96otkQIJnbzx7mBTsxxRq2qsR8ZWoef6AiaoL5dSDbwD_xrvklEmBKYNdm71c-F4zoXxii1NUP7KfRyqZdV_PcTnc5SDMc7OwDuf1IveDuOGiqqphLZtFxhyuG6i2inFv3BIB3Xhj8kRheJQJAD2CVMN_5W5e6K7KXfWEXz8vBfkc5vvW0Kyl-=w1280",
    "proj-09.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQUd_5xXuC8IrUDFlmajXCxmZOwjJoRJOf-291LOA5xsiAislU2io0Yt-mgDJGInD_OlC7HfRrIBugp8l_L6QmblmIKbYdECV5ENqKDTwlTmyFB_1a-Gr6GEaZnn75I9OuNU4TK6jbE5su68bU2xirtExnlodJ7SyCSe-UPTR9G777uD1SpCSTz1qaJUVIquAlhKCAIY5_ttiv_lx8uMCgV8HWmtH4-FxdT2DLefPEk=w1280",
    "proj-10.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQX_568aAQxco0DnDj0FIfRI1IjEkfYCb0V3MY5Yw-N51I22mbNtHYV4_rjHLfn3UfByIoJOPjtr21YVRzvknC2ECvbaqwMdXBhMFIWF8F0mO2GvE5PhBp6z6I_Bd8UEbSvalo4JYzIJ-8gQODOSp-m9Ymjimq-BRbS1PJA3PnLMm8FNisx-tf1_UCU8Tz6M-ypX5ooUH-6klo4N0LBOW32Y8ON9s4rT3VFaIUJkc=w1280",
    "proj-11.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQWlg8fOrtKUz77SV-1JVZ0jjfSsgLbLFUx9cQaFFRqNObJxN_7Ju9jux1QsvLEUtrR2kSP0Yv-6K2-CGrNiyoMGQ1Klbx_UqA0xpD1us7zFkIO7eRNkdl-iH3fZX5NMJdJLtSWqselNsajm2hq-nBYJngxXV1Z8B2WcxfORVz30Z6lKfI3k46JwNabPhboSl2i3xHh6lncchKWtnE8-r0x5lFqIRxAHDqGdAHYLDZU=w1280",
    "proj-12.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQV7HMLJ-U2h-tO8kyEtu5wI99DVBO0Qg9V57zXIQfdeTVLS4uvZy7nuRTWnrK26gWkqJzJKfmOaTOMUG6nSmiFXXryJCZjWBa8Qj9pu7mKsssChmfVRHyZWy_7NnzItUr7GiixIgEopw76wWqFlQNlqFOAHVwtWK3FE4vXjnGB0bJpNT3vwkEuq0tDS6-NwVbCDe2_NgMoPwsD91-fEoy-7fAFiwP8CV94KWKj=w1280",
    "proj-13.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQVZJxiRo66XG82vX9WmKx2s7ZcO4jIZjjcefyIKaZiwP-YoO4twcfTcEa8AG5U7J2Kssa5Iz_DfAIHi9w5jp78yOZac6QCt2qhFyxj0iI9aZtXyY-qSYLujnL-4aQj7d6CxZenNz-OFMiYC_rSTdHKB7W0hhpqQpYx6Fo1ID5JrbbpvtYHxssBnkHOE4-4J-2cZvaajyJH1ZKty9xViBhhFh2VPS_5KeJh9aIeo3Ao=w1280",
    "proj-14.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQWZH6wmcqOjXWCMOmnx35vWZdRkfN2aLjQaYb_y8pjXQGLTGx_ic6QELrgqKLja0tOs_I1LQ4sCNcD1c-l1tcWt-EhXbAAdO-n2lN-cdnO8XYF3Xt4A--_MNehXmE2q7jMMi8iuRq-OwXbBGXM7vrHArU8ujORiGlfhGIon5QhA_p-CGMz-j-hP6EYCKDETENux17g6-69SDgIm2gZn5b2MDdbzRvj-TqX-J8uZY=w1280",
    "proj-15.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQW116az7rajh3-6IMUlxV_HuPEUAaY0Eg6MmwL6wWHX_sIOGP1ZXVEuyLod9j1r0--MUVx-yf7W6IeiPe3PirxlUZ1-lEUf4FuiaLm6Hx0r0KiPgt241vDywyG7mTF3sDVtHj6GyN_bzleAA0Hj-Hqh8LS0koRCXuVEhx02ysIYIER8v6fEMdZnlP1KMi6aKIGo_yh7oo06ZHO1LW_OksmicvIv3H6F5UDqjPoY=w1280",
    "proj-16.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQWaTByC7tAhT5ah4Xn_WoKr77bkfMPQB_zDPzGoLz_TLGuVkXCkNCZw7VM6XVrdVJOy0D-Y_x6UAxyRFESVDWPBcdJIEWZxyrjp2Y0Var8cVRwPZxnIk1ryoYxUVrmcg7wLYppAuOf3lnqxiRBBqhIhi0QW_dg4M8VqSyk5mp42XCIYx5d8zOaXhfxDZbUXG3hMLzqGpcuX52ZYaD7PraDuTHT9IXePt5xX6B5zXrU=w1280",
    "proj-17.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQX5kLdpXJ8HbI-cyGkM6sp-26x2QzWaADeM72C3TVfMQhLZjKESvNAs2Ve2FJYQyvWWSCc7HpzkXwjFxaQeTny1ViUDIxqbUiiTRvq12qnE05CHX6Wwcnf8GvJHoz3zxsjiivOU6yGrrhaYGWnRrOnksVJg4-ippjHVodT609RcYSn5bqR0WjxP4koAQk53jy3KndMpFJ4wsecoxVkI3spD_lrGYaaxHkDUg1extHk=w1280",
    "proj-18.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQVxP__YjonhtRfg2dzZtCYa4pvFPQMSGbaKl49D9ErOC6Eqd9re42k-5PlczrBgA_cj5ru86TXWmVUixvO9yFkFw2fbscM1v6CxjO7citrecrtlW6T0Sz1-cgAmFVHP3csFVOL1XT8jI90ckrelsB3NcerGDMWIITmtjrLYK8CPrDCxv8PDYyJyAbc7ZBE4mNYYdKsGE8bjL49yDSnb_vSx_Z6UvPSwC_73XCtD=w1280",
    "proj-19.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQUyvNlzwCgwoqA1pqQ-LiurOV02ck5bP3bm0o3JqZDcgEjeDQAoD0gJjzZlynXBqO7ALISuy9OI8_v9P1AUf3jbVuYdIcWhvlJ8ktykT-9xxiNIcenzgBf7zPYmAEuETzJ3iQd0T6q3uw5Z2X1Ig9-69UeJVLFwXZH8Tz6Ozc9wZ3XuLFQvr-5lucRakgQgNwZlwNldfrfG4qKmxHZXwnbN_uSDdL1Tpn4STMHTx3Y=w1280",
    "proj-20.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQVcmUq2paDIVwz7lA9-BLYwpx0H14dfEk8f7fR4Fzg39DJB9hb6t3nSyrrH_CI0yCZ6eSYhX8YpgB97eeavZYpLDGLQ5sXUHFFB0Vby0FBndYUUzaQOewaCHg4s1UYA4RRtPwhfPN_xAYwces98vX86RysVtXNTShAWAhebcHrLKHUMYEXW46LfdyQL-zBXJVukeVsmWrpLfMOCm5-GXUtLSFRg85_SrqqGgsGnR8g=w1280",
    "proj-21.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXqm4s4jLI1VwyBDi4G_p9fw00GgMT4H0N0q7AXQXZmXGzI79B-l77hGDEIfFiyWH0CYgr86EPeDkFuUrhOUI4ct6Qre0LnKDgWBbX6Xe7M6XQNBooC1hYGD7RcOyhynRtik9-blHL7W8pGf7VAr5_PrkyjKyUnAP1d-vlbN2awk9zY_Q6rqpN-OXZcmyXR9NlmO5HA9nEcGeYE_cVk4X9o1DaHJk70fn_I1j3d_QE=w1280",
    "proj-22.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXxp3t-HqNz_avROc5LTixi5hqRO_uZmJnfonJ2sYwYe-TTFcwvjMUUDO8k9sGLB63PsGER4C9ZvO-oUnTtPUp9kJAdjStGjfZwNVfwLkf8MZB2C-EWDFyZIouia-Lj9lVqvzbMPA2BbvZH6CvRoLLhPAtYBxBwOKQ0mUqaTyZkeJSTMsEvkA2By_5MYArmB4xzbLQktMIlvB7iIvjLbtP0jE7AXKp52-RRfA=w1280",
    "proj-23.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQUULdYBtDqaIbG_Al8mW1xgjwqlLjuFYHJaqTCQdnrUVwQXMtctYUlJLC2sMli4ZmecEXZhNN3sUJzc-A1e9T0f1I9Ljb2ovm4ScpWPnRfZSyoCJlTfwtN1cyq_0wY23OXkk08fXb-8mh6grVDf5FeHqp9blsHph_mrt6ApYlLyjuVN0xiQ0xRG-w-D3yRzN0Id218i9R8UfEAW3diD4y0PWIN7vg9b3VOktKZ5evA=w1280",
    "proj-24.jpg": "https://lh3.googleusercontent.com/sitesv/AG8ngQXGQBs6DzWUqCGwag_0H-blfsG1wHyN01zBZqcS8qO30CDtzM1JVoFBcSuE1kHAl7-mcSo5vMLDwX36TkuDggEdM76Z3UDvU4KJrfLOUs1E41pjb4AnpcJReXRbSTo80c4rsilKGut1174_V7eOs9SJ7WO_-diR5phcN9yudCmCx1tNHU438oowLOee1eUXL18_SHIVhMSdUAeuB6aultT3S9_PW7HoNlH9f-YdgJs=w1280",
}

def main():
    print("\n=== Wall Envy Asset Downloader ===\n")
    
    ok = fail = 0
    
    print("Brand images:")
    for filename, url in BRAND_IMAGES.items():
        dest = os.path.join(IMAGES_DIR, filename)
        if download(url, dest, filename):
            ok += 1
        else:
            fail += 1
        time.sleep(0.3)

    print("\nProject gallery images:")
    for filename, url in PROJECT_IMAGES.items():
        dest = os.path.join(PROJECTS_DIR, filename)
        if download(url, dest, filename):
            ok += 1
        else:
            fail += 1
        time.sleep(0.3)

    print(f"\n=== Done: {ok} downloaded, {fail} failed ===\n")

if __name__ == "__main__":
    main()
