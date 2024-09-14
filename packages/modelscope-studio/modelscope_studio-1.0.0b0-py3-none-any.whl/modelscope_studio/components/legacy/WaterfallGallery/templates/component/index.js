var Ea = Object.defineProperty;
var Ta = (n, e, t) => e in n ? Ea(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t;
var li = (n, e, t) => Ta(n, typeof e != "symbol" ? e + "" : e, t);
const {
  SvelteComponent: ya,
  assign: Aa,
  create_slot: Sa,
  detach: Ca,
  element: La,
  get_all_dirty_from_scope: Ra,
  get_slot_changes: Ia,
  get_spread_update: Da,
  init: Oa,
  insert: Na,
  safe_not_equal: Ma,
  set_dynamic_element_data: ii,
  set_style: pe,
  toggle_class: je,
  transition_in: To,
  transition_out: yo,
  update_slot_base: Pa
} = window.__gradio__svelte__internal;
function Fa(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), o = Sa(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [{
    "data-testid": (
      /*test_id*/
      n[7]
    )
  }, {
    id: (
      /*elem_id*/
      n[2]
    )
  }, {
    class: t = "block " + /*elem_classes*/
    n[3].join(" ") + " svelte-nl1om8"
  }], f = {};
  for (let r = 0; r < s.length; r += 1)
    f = Aa(f, s[r]);
  return {
    c() {
      e = La(
        /*tag*/
        n[14]
      ), o && o.c(), ii(
        /*tag*/
        n[14]
      )(e, f), je(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), je(
        e,
        "padded",
        /*padding*/
        n[6]
      ), je(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), je(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), je(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), pe(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), pe(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), pe(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), pe(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), pe(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), pe(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), pe(e, "border-width", "var(--block-border-width)");
    },
    m(r, a) {
      Na(r, e, a), o && o.m(e, null), l = !0;
    },
    p(r, a) {
      o && o.p && (!l || a & /*$$scope*/
      131072) && Pa(
        o,
        i,
        r,
        /*$$scope*/
        r[17],
        l ? Ia(
          i,
          /*$$scope*/
          r[17],
          a,
          null
        ) : Ra(
          /*$$scope*/
          r[17]
        ),
        null
      ), ii(
        /*tag*/
        r[14]
      )(e, f = Da(s, [(!l || a & /*test_id*/
      128) && {
        "data-testid": (
          /*test_id*/
          r[7]
        )
      }, (!l || a & /*elem_id*/
      4) && {
        id: (
          /*elem_id*/
          r[2]
        )
      }, (!l || a & /*elem_classes*/
      8 && t !== (t = "block " + /*elem_classes*/
      r[3].join(" ") + " svelte-nl1om8")) && {
        class: t
      }])), je(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), je(
        e,
        "padded",
        /*padding*/
        r[6]
      ), je(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), je(
        e,
        "border_contrast",
        /*border_mode*/
        r[5] === "contrast"
      ), je(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), a & /*height*/
      1 && pe(
        e,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), a & /*width*/
      2 && pe(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), a & /*variant*/
      16 && pe(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), a & /*allow_overflow*/
      2048 && pe(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && pe(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), a & /*min_width*/
      8192 && pe(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (To(o, r), l = !0);
    },
    o(r) {
      yo(o, r), l = !1;
    },
    d(r) {
      r && Ca(e), o && o.d(r);
    }
  };
}
function Ua(n) {
  let e, t = (
    /*tag*/
    n[14] && Fa(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (To(t, l), e = !0);
    },
    o(l) {
      yo(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function za(n, e, t) {
  let {
    $$slots: l = {},
    $$scope: i
  } = e, {
    height: o = void 0
  } = e, {
    width: s = void 0
  } = e, {
    elem_id: f = ""
  } = e, {
    elem_classes: r = []
  } = e, {
    variant: a = "solid"
  } = e, {
    border_mode: c = "base"
  } = e, {
    padding: u = !0
  } = e, {
    type: d = "normal"
  } = e, {
    test_id: h = void 0
  } = e, {
    explicit_call: p = !1
  } = e, {
    container: y = !0
  } = e, {
    visible: L = !0
  } = e, {
    allow_overflow: E = !0
  } = e, {
    scale: g = null
  } = e, {
    min_width: v = 0
  } = e, b = d === "fieldset" ? "fieldset" : "div";
  const S = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return n.$$set = (w) => {
    "height" in w && t(0, o = w.height), "width" in w && t(1, s = w.width), "elem_id" in w && t(2, f = w.elem_id), "elem_classes" in w && t(3, r = w.elem_classes), "variant" in w && t(4, a = w.variant), "border_mode" in w && t(5, c = w.border_mode), "padding" in w && t(6, u = w.padding), "type" in w && t(16, d = w.type), "test_id" in w && t(7, h = w.test_id), "explicit_call" in w && t(8, p = w.explicit_call), "container" in w && t(9, y = w.container), "visible" in w && t(10, L = w.visible), "allow_overflow" in w && t(11, E = w.allow_overflow), "scale" in w && t(12, g = w.scale), "min_width" in w && t(13, v = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [o, s, f, r, a, c, u, h, p, y, L, E, g, v, b, S, d, i, l];
}
class qa extends ya {
  constructor(e) {
    super(), Oa(this, e, za, Ua, Ma, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Ha,
  append: Zn,
  attr: gn,
  create_component: Ba,
  destroy_component: ja,
  detach: Wa,
  element: oi,
  init: Ga,
  insert: Va,
  mount_component: Ya,
  safe_not_equal: Xa,
  set_data: Za,
  space: Ka,
  text: Ja,
  toggle_class: st,
  transition_in: Qa,
  transition_out: xa
} = window.__gradio__svelte__internal;
function $a(n) {
  let e, t, l, i, o, s;
  return l = new /*Icon*/
  n[1]({}), {
    c() {
      e = oi("label"), t = oi("span"), Ba(l.$$.fragment), i = Ka(), o = Ja(
        /*label*/
        n[0]
      ), gn(t, "class", "svelte-9gxdi0"), gn(e, "for", ""), gn(e, "data-testid", "block-label"), gn(e, "class", "svelte-9gxdi0"), st(e, "hide", !/*show_label*/
      n[2]), st(e, "sr-only", !/*show_label*/
      n[2]), st(
        e,
        "float",
        /*float*/
        n[4]
      ), st(
        e,
        "hide-label",
        /*disable*/
        n[3]
      );
    },
    m(f, r) {
      Va(f, e, r), Zn(e, t), Ya(l, t, null), Zn(e, i), Zn(e, o), s = !0;
    },
    p(f, [r]) {
      (!s || r & /*label*/
      1) && Za(
        o,
        /*label*/
        f[0]
      ), (!s || r & /*show_label*/
      4) && st(e, "hide", !/*show_label*/
      f[2]), (!s || r & /*show_label*/
      4) && st(e, "sr-only", !/*show_label*/
      f[2]), (!s || r & /*float*/
      16) && st(
        e,
        "float",
        /*float*/
        f[4]
      ), (!s || r & /*disable*/
      8) && st(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      s || (Qa(l.$$.fragment, f), s = !0);
    },
    o(f) {
      xa(l.$$.fragment, f), s = !1;
    },
    d(f) {
      f && Wa(e), ja(l);
    }
  };
}
function er(n, e, t) {
  let {
    label: l = null
  } = e, {
    Icon: i
  } = e, {
    show_label: o = !0
  } = e, {
    disable: s = !1
  } = e, {
    float: f = !0
  } = e;
  return n.$$set = (r) => {
    "label" in r && t(0, l = r.label), "Icon" in r && t(1, i = r.Icon), "show_label" in r && t(2, o = r.show_label), "disable" in r && t(3, s = r.disable), "float" in r && t(4, f = r.float);
  }, [l, i, o, s, f];
}
class tr extends Ha {
  constructor(e) {
    super(), Ga(this, e, er, $a, Xa, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: nr,
  append: El,
  attr: $e,
  bubble: lr,
  create_component: ir,
  destroy_component: or,
  detach: Ao,
  element: Tl,
  init: ar,
  insert: So,
  listen: rr,
  mount_component: sr,
  safe_not_equal: fr,
  set_data: cr,
  set_style: Ct,
  space: ur,
  text: _r,
  toggle_class: de,
  transition_in: dr,
  transition_out: mr
} = window.__gradio__svelte__internal;
function ai(n) {
  let e, t;
  return {
    c() {
      e = Tl("span"), t = _r(
        /*label*/
        n[1]
      ), $e(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      So(l, e, i), El(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && cr(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Ao(e);
    }
  };
}
function hr(n) {
  let e, t, l, i, o, s, f, r = (
    /*show_label*/
    n[2] && ai(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Tl("button"), r && r.c(), t = ur(), l = Tl("div"), ir(i.$$.fragment), $e(l, "class", "svelte-1lrphxw"), de(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), de(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), de(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], $e(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), $e(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), $e(
        e,
        "title",
        /*label*/
        n[1]
      ), $e(e, "class", "svelte-1lrphxw"), de(
        e,
        "pending",
        /*pending*/
        n[3]
      ), de(
        e,
        "padded",
        /*padded*/
        n[5]
      ), de(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), de(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), Ct(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), Ct(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), Ct(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(a, c) {
      So(a, e, c), r && r.m(e, null), El(e, t), El(e, l), sr(i, l, null), o = !0, s || (f = rr(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), s = !0);
    },
    p(a, [c]) {
      /*show_label*/
      a[2] ? r ? r.p(a, c) : (r = ai(a), r.c(), r.m(e, t)) : r && (r.d(1), r = null), (!o || c & /*size*/
      16) && de(
        l,
        "small",
        /*size*/
        a[4] === "small"
      ), (!o || c & /*size*/
      16) && de(
        l,
        "large",
        /*size*/
        a[4] === "large"
      ), (!o || c & /*size*/
      16) && de(
        l,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!o || c & /*label*/
      2) && $e(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!o || c & /*hasPopup*/
      256) && $e(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!o || c & /*label*/
      2) && $e(
        e,
        "title",
        /*label*/
        a[1]
      ), (!o || c & /*pending*/
      8) && de(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!o || c & /*padded*/
      32) && de(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!o || c & /*highlight*/
      64) && de(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!o || c & /*transparent*/
      512) && de(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), c & /*disabled, _color*/
      4224 && Ct(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && Ct(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), c & /*offset*/
      2048 && Ct(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      o || (dr(i.$$.fragment, a), o = !0);
    },
    o(a) {
      mr(i.$$.fragment, a), o = !1;
    },
    d(a) {
      a && Ao(e), r && r.d(), or(i), s = !1, f();
    }
  };
}
function gr(n, e, t) {
  let l, {
    Icon: i
  } = e, {
    label: o = ""
  } = e, {
    show_label: s = !1
  } = e, {
    pending: f = !1
  } = e, {
    size: r = "small"
  } = e, {
    padded: a = !0
  } = e, {
    highlight: c = !1
  } = e, {
    disabled: u = !1
  } = e, {
    hasPopup: d = !1
  } = e, {
    color: h = "var(--block-label-text-color)"
  } = e, {
    transparent: p = !1
  } = e, {
    background: y = "var(--background-fill-primary)"
  } = e, {
    offset: L = 0
  } = e;
  function E(g) {
    lr.call(this, n, g);
  }
  return n.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, o = g.label), "show_label" in g && t(2, s = g.show_label), "pending" in g && t(3, f = g.pending), "size" in g && t(4, r = g.size), "padded" in g && t(5, a = g.padded), "highlight" in g && t(6, c = g.highlight), "disabled" in g && t(7, u = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, h = g.color), "transparent" in g && t(9, p = g.transparent), "background" in g && t(10, y = g.background), "offset" in g && t(11, L = g.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = c ? "var(--color-accent)" : h);
  }, [i, o, s, f, r, a, c, u, d, p, y, L, l, h, E];
}
let dt = class extends nr {
  constructor(e) {
    super(), ar(this, e, gr, hr, fr, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
};
const {
  SvelteComponent: br,
  append: pr,
  attr: Kn,
  binding_callbacks: wr,
  create_slot: kr,
  detach: vr,
  element: ri,
  get_all_dirty_from_scope: Er,
  get_slot_changes: Tr,
  init: yr,
  insert: Ar,
  safe_not_equal: Sr,
  toggle_class: ft,
  transition_in: Cr,
  transition_out: Lr,
  update_slot_base: Rr
} = window.__gradio__svelte__internal;
function Ir(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[5].default
  ), o = kr(
    i,
    n,
    /*$$scope*/
    n[4],
    null
  );
  return {
    c() {
      e = ri("div"), t = ri("div"), o && o.c(), Kn(t, "class", "icon svelte-3w3rth"), Kn(e, "class", "empty svelte-3w3rth"), Kn(e, "aria-label", "Empty value"), ft(
        e,
        "small",
        /*size*/
        n[0] === "small"
      ), ft(
        e,
        "large",
        /*size*/
        n[0] === "large"
      ), ft(
        e,
        "unpadded_box",
        /*unpadded_box*/
        n[1]
      ), ft(
        e,
        "small_parent",
        /*parent_height*/
        n[3]
      );
    },
    m(s, f) {
      Ar(s, e, f), pr(e, t), o && o.m(t, null), n[6](e), l = !0;
    },
    p(s, [f]) {
      o && o.p && (!l || f & /*$$scope*/
      16) && Rr(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        l ? Tr(
          i,
          /*$$scope*/
          s[4],
          f,
          null
        ) : Er(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!l || f & /*size*/
      1) && ft(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!l || f & /*size*/
      1) && ft(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!l || f & /*unpadded_box*/
      2) && ft(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!l || f & /*parent_height*/
      8) && ft(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      l || (Cr(o, s), l = !0);
    },
    o(s) {
      Lr(o, s), l = !1;
    },
    d(s) {
      s && vr(e), o && o.d(s), n[6](null);
    }
  };
}
function Dr(n, e, t) {
  let l, {
    $$slots: i = {},
    $$scope: o
  } = e, {
    size: s = "small"
  } = e, {
    unpadded_box: f = !1
  } = e, r;
  function a(u) {
    var p;
    if (!u) return !1;
    const {
      height: d
    } = u.getBoundingClientRect(), {
      height: h
    } = ((p = u.parentElement) == null ? void 0 : p.getBoundingClientRect()) || {
      height: d
    };
    return d > h + 2;
  }
  function c(u) {
    wr[u ? "unshift" : "push"](() => {
      r = u, t(2, r);
    });
  }
  return n.$$set = (u) => {
    "size" in u && t(0, s = u.size), "unpadded_box" in u && t(1, f = u.unpadded_box), "$$scope" in u && t(4, o = u.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*el*/
    4 && t(3, l = a(r));
  }, [s, f, r, l, o, i, c];
}
class Or extends br {
  constructor(e) {
    super(), yr(this, e, Dr, Ir, Sr, {
      size: 0,
      unpadded_box: 1
    });
  }
}
const {
  SvelteComponent: Nr,
  append: Jn,
  attr: Le,
  detach: Mr,
  init: Pr,
  insert: Fr,
  noop: Qn,
  safe_not_equal: Ur,
  set_style: We,
  svg_element: bn
} = window.__gradio__svelte__internal;
function zr(n) {
  let e, t, l, i;
  return {
    c() {
      e = bn("svg"), t = bn("g"), l = bn("path"), i = bn("path"), Le(l, "d", "M18,6L6.087,17.913"), We(l, "fill", "none"), We(l, "fill-rule", "nonzero"), We(l, "stroke-width", "2px"), Le(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Le(i, "d", "M4.364,4.364L19.636,19.636"), We(i, "fill", "none"), We(i, "fill-rule", "nonzero"), We(i, "stroke-width", "2px"), Le(e, "width", "100%"), Le(e, "height", "100%"), Le(e, "viewBox", "0 0 24 24"), Le(e, "version", "1.1"), Le(e, "xmlns", "http://www.w3.org/2000/svg"), Le(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Le(e, "xml:space", "preserve"), Le(e, "stroke", "currentColor"), We(e, "fill-rule", "evenodd"), We(e, "clip-rule", "evenodd"), We(e, "stroke-linecap", "round"), We(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      Fr(o, e, s), Jn(e, t), Jn(t, l), Jn(e, i);
    },
    p: Qn,
    i: Qn,
    o: Qn,
    d(o) {
      o && Mr(e);
    }
  };
}
let qr = class extends Nr {
  constructor(e) {
    super(), Pr(this, e, null, zr, Ur, {});
  }
};
const {
  SvelteComponent: Hr,
  append: Br,
  attr: Yt,
  detach: jr,
  init: Wr,
  insert: Gr,
  noop: xn,
  safe_not_equal: Vr,
  svg_element: si
} = window.__gradio__svelte__internal;
function Yr(n) {
  let e, t;
  return {
    c() {
      e = si("svg"), t = si("path"), Yt(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), Yt(t, "fill", "currentColor"), Yt(e, "id", "icon"), Yt(e, "xmlns", "http://www.w3.org/2000/svg"), Yt(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      Gr(l, e, i), Br(e, t);
    },
    p: xn,
    i: xn,
    o: xn,
    d(l) {
      l && jr(e);
    }
  };
}
class Xr extends Hr {
  constructor(e) {
    super(), Wr(this, e, null, Yr, Vr, {});
  }
}
const {
  SvelteComponent: Zr,
  append: Kr,
  attr: Lt,
  detach: Jr,
  init: Qr,
  insert: xr,
  noop: $n,
  safe_not_equal: $r,
  svg_element: fi
} = window.__gradio__svelte__internal;
function es(n) {
  let e, t;
  return {
    c() {
      e = fi("svg"), t = fi("path"), Lt(t, "fill", "currentColor"), Lt(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Lt(e, "xmlns", "http://www.w3.org/2000/svg"), Lt(e, "width", "100%"), Lt(e, "height", "100%"), Lt(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      xr(l, e, i), Kr(e, t);
    },
    p: $n,
    i: $n,
    o: $n,
    d(l) {
      l && Jr(e);
    }
  };
}
class Co extends Zr {
  constructor(e) {
    super(), Qr(this, e, null, es, $r, {});
  }
}
const {
  SvelteComponent: ts,
  append: ns,
  attr: Re,
  detach: ls,
  init: is,
  insert: os,
  noop: el,
  safe_not_equal: as,
  svg_element: ci
} = window.__gradio__svelte__internal;
function rs(n) {
  let e, t;
  return {
    c() {
      e = ci("svg"), t = ci("path"), Re(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), Re(e, "xmlns", "http://www.w3.org/2000/svg"), Re(e, "width", "100%"), Re(e, "height", "100%"), Re(e, "viewBox", "0 0 24 24"), Re(e, "fill", "none"), Re(e, "stroke", "currentColor"), Re(e, "stroke-width", "1.5"), Re(e, "stroke-linecap", "round"), Re(e, "stroke-linejoin", "round"), Re(e, "class", "feather feather-edit-2");
    },
    m(l, i) {
      os(l, e, i), ns(e, t);
    },
    p: el,
    i: el,
    o: el,
    d(l) {
      l && ls(e);
    }
  };
}
class ss extends ts {
  constructor(e) {
    super(), is(this, e, null, rs, as, {});
  }
}
const {
  SvelteComponent: fs,
  append: tl,
  attr: K,
  detach: cs,
  init: us,
  insert: _s,
  noop: nl,
  safe_not_equal: ds,
  svg_element: pn
} = window.__gradio__svelte__internal;
function ms(n) {
  let e, t, l, i;
  return {
    c() {
      e = pn("svg"), t = pn("rect"), l = pn("circle"), i = pn("polyline"), K(t, "x", "3"), K(t, "y", "3"), K(t, "width", "18"), K(t, "height", "18"), K(t, "rx", "2"), K(t, "ry", "2"), K(l, "cx", "8.5"), K(l, "cy", "8.5"), K(l, "r", "1.5"), K(i, "points", "21 15 16 10 5 21"), K(e, "xmlns", "http://www.w3.org/2000/svg"), K(e, "width", "100%"), K(e, "height", "100%"), K(e, "viewBox", "0 0 24 24"), K(e, "fill", "none"), K(e, "stroke", "currentColor"), K(e, "stroke-width", "1.5"), K(e, "stroke-linecap", "round"), K(e, "stroke-linejoin", "round"), K(e, "class", "feather feather-image");
    },
    m(o, s) {
      _s(o, e, s), tl(e, t), tl(e, l), tl(e, i);
    },
    p: nl,
    i: nl,
    o: nl,
    d(o) {
      o && cs(e);
    }
  };
}
let Lo = class extends fs {
  constructor(e) {
    super(), us(this, e, null, ms, ds, {});
  }
};
const {
  SvelteComponent: hs,
  append: ui,
  attr: ae,
  detach: gs,
  init: bs,
  insert: ps,
  noop: _i,
  safe_not_equal: ws,
  svg_element: ll
} = window.__gradio__svelte__internal;
function ks(n) {
  let e, t, l, i;
  return {
    c() {
      e = ll("svg"), t = ll("path"), l = ll("path"), ae(t, "stroke", "currentColor"), ae(t, "stroke-width", "1.5"), ae(t, "stroke-linecap", "round"), ae(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), ae(l, "stroke", "currentColor"), ae(l, "stroke-width", "1.5"), ae(l, "stroke-linecap", "round"), ae(l, "stroke-linejoin", "round"), ae(l, "d", "M7 20V9"), ae(e, "xmlns", "http://www.w3.org/2000/svg"), ae(e, "viewBox", "0 0 24 24"), ae(e, "fill", i = /*selected*/
      n[0] ? "currentColor" : "none"), ae(e, "stroke-width", "1.5"), ae(e, "color", "currentColor");
    },
    m(o, s) {
      ps(o, e, s), ui(e, t), ui(e, l);
    },
    p(o, [s]) {
      s & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && ae(e, "fill", i);
    },
    i: _i,
    o: _i,
    d(o) {
      o && gs(e);
    }
  };
}
function vs(n, e, t) {
  let {
    selected: l
  } = e;
  return n.$$set = (i) => {
    "selected" in i && t(0, l = i.selected);
  }, [l];
}
class Es extends hs {
  constructor(e) {
    super(), bs(this, e, vs, ks, ws, {
      selected: 0
    });
  }
}
const {
  SvelteComponent: Ts,
  append: di,
  attr: Ee,
  detach: ys,
  init: As,
  insert: Ss,
  noop: il,
  safe_not_equal: Cs,
  svg_element: ol
} = window.__gradio__svelte__internal;
function Ls(n) {
  let e, t, l;
  return {
    c() {
      e = ol("svg"), t = ol("polyline"), l = ol("path"), Ee(t, "points", "1 4 1 10 7 10"), Ee(l, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), Ee(e, "xmlns", "http://www.w3.org/2000/svg"), Ee(e, "width", "100%"), Ee(e, "height", "100%"), Ee(e, "viewBox", "0 0 24 24"), Ee(e, "fill", "none"), Ee(e, "stroke", "currentColor"), Ee(e, "stroke-width", "2"), Ee(e, "stroke-linecap", "round"), Ee(e, "stroke-linejoin", "round"), Ee(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      Ss(i, e, o), di(e, t), di(e, l);
    },
    p: il,
    i: il,
    o: il,
    d(i) {
      i && ys(e);
    }
  };
}
class Rs extends Ts {
  constructor(e) {
    super(), As(this, e, null, Ls, Cs, {});
  }
}
const Is = [{
  color: "red",
  primary: 600,
  secondary: 100
}, {
  color: "green",
  primary: 600,
  secondary: 100
}, {
  color: "blue",
  primary: 600,
  secondary: 100
}, {
  color: "yellow",
  primary: 500,
  secondary: 100
}, {
  color: "purple",
  primary: 600,
  secondary: 100
}, {
  color: "teal",
  primary: 600,
  secondary: 100
}, {
  color: "orange",
  primary: 600,
  secondary: 100
}, {
  color: "cyan",
  primary: 600,
  secondary: 100
}, {
  color: "lime",
  primary: 500,
  secondary: 100
}, {
  color: "pink",
  primary: 600,
  secondary: 100
}], mi = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Is.reduce((n, {
  color: e,
  primary: t,
  secondary: l
}) => ({
  ...n,
  [e]: {
    primary: mi[e][t],
    secondary: mi[e][l]
  }
}), {});
class Ds extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Os,
  create_component: Ns,
  destroy_component: Ms,
  init: Ps,
  mount_component: Fs,
  safe_not_equal: Us,
  transition_in: zs,
  transition_out: qs
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Hs
} = window.__gradio__svelte__internal;
function Bs(n) {
  let e, t;
  return e = new dt({
    props: {
      Icon: Xr,
      label: (
        /*i18n*/
        n[2]("common.share")
      ),
      pending: (
        /*pending*/
        n[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[5]
  ), {
    c() {
      Ns(e.$$.fragment);
    },
    m(l, i) {
      Fs(e, l, i), t = !0;
    },
    p(l, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      l[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      l[3]), e.$set(o);
    },
    i(l) {
      t || (zs(e.$$.fragment, l), t = !0);
    },
    o(l) {
      qs(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ms(e, l);
    }
  };
}
function js(n, e, t) {
  const l = Hs();
  let {
    formatter: i
  } = e, {
    value: o
  } = e, {
    i18n: s
  } = e, f = !1;
  const r = async () => {
    try {
      t(3, f = !0);
      const a = await i(o);
      l("share", {
        description: a
      });
    } catch (a) {
      console.error(a);
      let c = a instanceof Ds ? a.message : "Share failed.";
      l("error", c);
    } finally {
      t(3, f = !1);
    }
  };
  return n.$$set = (a) => {
    "formatter" in a && t(0, i = a.formatter), "value" in a && t(1, o = a.value), "i18n" in a && t(2, s = a.i18n);
  }, [i, o, s, f, l, r];
}
class Ws extends Os {
  constructor(e) {
    super(), Ps(this, e, js, Bs, Us, {
      formatter: 0,
      value: 1,
      i18n: 2
    });
  }
}
function Dt(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function An() {
}
function Gs(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Ro = typeof window < "u";
let hi = Ro ? () => window.performance.now() : () => Date.now(), Io = Ro ? (n) => requestAnimationFrame(n) : An;
const Mt = /* @__PURE__ */ new Set();
function Do(n) {
  Mt.forEach((e) => {
    e.c(n) || (Mt.delete(e), e.f());
  }), Mt.size !== 0 && Io(Do);
}
function Vs(n) {
  let e;
  return Mt.size === 0 && Io(Do), {
    promise: new Promise((t) => {
      Mt.add(e = {
        c: n,
        f: t
      });
    }),
    abort() {
      Mt.delete(e);
    }
  };
}
const Rt = [];
function Ys(n, e = An) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(f) {
    if (Gs(n, f) && (n = f, t)) {
      const r = !Rt.length;
      for (const a of l)
        a[1](), Rt.push(a, n);
      if (r) {
        for (let a = 0; a < Rt.length; a += 2)
          Rt[a][0](Rt[a + 1]);
        Rt.length = 0;
      }
    }
  }
  function o(f) {
    i(f(n));
  }
  function s(f, r = An) {
    const a = [f, r];
    return l.add(a), l.size === 1 && (t = e(i, o) || An), f(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: s
  };
}
function gi(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function yl(n, e, t, l) {
  if (typeof t == "number" || gi(t)) {
    const i = l - t, o = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, f = n.opts.damping * o, r = (s - f) * n.inv_mass, a = (o + r) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, gi(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map((i, o) => yl(n, e[o], t[o], l[o]));
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = yl(n, e[o], t[o], l[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function bi(n, e = {}) {
  const t = Ys(n), {
    stiffness: l = 0.15,
    damping: i = 0.8,
    precision: o = 0.01
  } = e;
  let s, f, r, a = n, c = n, u = 1, d = 0, h = !1;
  function p(L, E = {}) {
    c = L;
    const g = r = {};
    return n == null || E.hard || y.stiffness >= 1 && y.damping >= 1 ? (h = !0, s = hi(), a = L, t.set(n = c), Promise.resolve()) : (E.soft && (d = 1 / ((E.soft === !0 ? 0.5 : +E.soft) * 60), u = 0), f || (s = hi(), h = !1, f = Vs((v) => {
      if (h)
        return h = !1, f = null, !1;
      u = Math.min(u + d, 1);
      const b = {
        inv_mass: u,
        opts: y,
        settled: !0,
        dt: (v - s) * 60 / 1e3
      }, S = yl(b, a, n, c);
      return s = v, a = n, t.set(n = S), b.settled && (f = null), !b.settled;
    })), new Promise((v) => {
      f.promise.then(() => {
        g === r && v();
      });
    }));
  }
  const y = {
    set: p,
    update: (L, E) => p(L(c, n), E),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: Xs,
  append: Ie,
  attr: P,
  component_subscribe: pi,
  detach: Zs,
  element: Ks,
  init: Js,
  insert: Qs,
  noop: wi,
  safe_not_equal: xs,
  set_style: wn,
  svg_element: De,
  toggle_class: ki
} = window.__gradio__svelte__internal, {
  onMount: $s
} = window.__gradio__svelte__internal;
function ef(n) {
  let e, t, l, i, o, s, f, r, a, c, u, d;
  return {
    c() {
      e = Ks("div"), t = De("svg"), l = De("g"), i = De("path"), o = De("path"), s = De("path"), f = De("path"), r = De("g"), a = De("path"), c = De("path"), u = De("path"), d = De("path"), P(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), P(i, "fill", "#FF7C00"), P(i, "fill-opacity", "0.4"), P(i, "class", "svelte-43sxxs"), P(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), P(o, "fill", "#FF7C00"), P(o, "class", "svelte-43sxxs"), P(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), P(s, "fill", "#FF7C00"), P(s, "fill-opacity", "0.4"), P(s, "class", "svelte-43sxxs"), P(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), P(f, "fill", "#FF7C00"), P(f, "class", "svelte-43sxxs"), wn(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), P(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), P(a, "fill", "#FF7C00"), P(a, "fill-opacity", "0.4"), P(a, "class", "svelte-43sxxs"), P(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), P(c, "fill", "#FF7C00"), P(c, "class", "svelte-43sxxs"), P(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), P(u, "fill", "#FF7C00"), P(u, "fill-opacity", "0.4"), P(u, "class", "svelte-43sxxs"), P(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), P(d, "fill", "#FF7C00"), P(d, "class", "svelte-43sxxs"), wn(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), P(t, "viewBox", "-1200 -1200 3000 3000"), P(t, "fill", "none"), P(t, "xmlns", "http://www.w3.org/2000/svg"), P(t, "class", "svelte-43sxxs"), P(e, "class", "svelte-43sxxs"), ki(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(h, p) {
      Qs(h, e, p), Ie(e, t), Ie(t, l), Ie(l, i), Ie(l, o), Ie(l, s), Ie(l, f), Ie(t, r), Ie(r, a), Ie(r, c), Ie(r, u), Ie(r, d);
    },
    p(h, [p]) {
      p & /*$top*/
      2 && wn(l, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), p & /*$bottom*/
      4 && wn(r, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), p & /*margin*/
      1 && ki(
        e,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: wi,
    o: wi,
    d(h) {
      h && Zs(e);
    }
  };
}
function tf(n, e, t) {
  let l, i, {
    margin: o = !0
  } = e;
  const s = bi([0, 0]);
  pi(n, s, (d) => t(1, l = d));
  const f = bi([0, 0]);
  pi(n, f, (d) => t(2, i = d));
  let r;
  async function a() {
    await Promise.all([s.set([125, 140]), f.set([-125, -140])]), await Promise.all([s.set([-125, 140]), f.set([125, -140])]), await Promise.all([s.set([-125, 0]), f.set([125, -0])]), await Promise.all([s.set([125, 0]), f.set([-125, 0])]);
  }
  async function c() {
    await a(), r || c();
  }
  async function u() {
    await Promise.all([s.set([125, 0]), f.set([-125, 0])]), c();
  }
  return $s(() => (u(), () => r = !0)), n.$$set = (d) => {
    "margin" in d && t(0, o = d.margin);
  }, [o, l, i, s, f];
}
class Oo extends Xs {
  constructor(e) {
    super(), Js(this, e, tf, ef, xs, {
      margin: 0
    });
  }
}
const {
  SvelteComponent: nf,
  append: Al,
  attr: et,
  bubble: lf,
  create_component: of,
  destroy_component: af,
  detach: No,
  element: Sl,
  init: rf,
  insert: Mo,
  listen: sf,
  mount_component: ff,
  safe_not_equal: cf,
  set_data: uf,
  set_style: It,
  space: _f,
  text: df,
  toggle_class: me,
  transition_in: mf,
  transition_out: hf
} = window.__gradio__svelte__internal;
function vi(n) {
  let e, t;
  return {
    c() {
      e = Sl("span"), t = df(
        /*label*/
        n[1]
      ), et(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      Mo(l, e, i), Al(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && uf(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && No(e);
    }
  };
}
function gf(n) {
  let e, t, l, i, o, s, f, r = (
    /*show_label*/
    n[2] && vi(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Sl("button"), r && r.c(), t = _f(), l = Sl("div"), of(i.$$.fragment), et(l, "class", "svelte-1lrphxw"), me(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), me(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), me(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], et(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), et(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), et(
        e,
        "title",
        /*label*/
        n[1]
      ), et(e, "class", "svelte-1lrphxw"), me(
        e,
        "pending",
        /*pending*/
        n[3]
      ), me(
        e,
        "padded",
        /*padded*/
        n[5]
      ), me(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), me(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), It(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), It(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), It(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(a, c) {
      Mo(a, e, c), r && r.m(e, null), Al(e, t), Al(e, l), ff(i, l, null), o = !0, s || (f = sf(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), s = !0);
    },
    p(a, [c]) {
      /*show_label*/
      a[2] ? r ? r.p(a, c) : (r = vi(a), r.c(), r.m(e, t)) : r && (r.d(1), r = null), (!o || c & /*size*/
      16) && me(
        l,
        "small",
        /*size*/
        a[4] === "small"
      ), (!o || c & /*size*/
      16) && me(
        l,
        "large",
        /*size*/
        a[4] === "large"
      ), (!o || c & /*size*/
      16) && me(
        l,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!o || c & /*label*/
      2) && et(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!o || c & /*hasPopup*/
      256) && et(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!o || c & /*label*/
      2) && et(
        e,
        "title",
        /*label*/
        a[1]
      ), (!o || c & /*pending*/
      8) && me(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!o || c & /*padded*/
      32) && me(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!o || c & /*highlight*/
      64) && me(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!o || c & /*transparent*/
      512) && me(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), c & /*disabled, _color*/
      4224 && It(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && It(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), c & /*offset*/
      2048 && It(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      o || (mf(i.$$.fragment, a), o = !0);
    },
    o(a) {
      hf(i.$$.fragment, a), o = !1;
    },
    d(a) {
      a && No(e), r && r.d(), af(i), s = !1, f();
    }
  };
}
function bf(n, e, t) {
  let l, {
    Icon: i
  } = e, {
    label: o = ""
  } = e, {
    show_label: s = !1
  } = e, {
    pending: f = !1
  } = e, {
    size: r = "small"
  } = e, {
    padded: a = !0
  } = e, {
    highlight: c = !1
  } = e, {
    disabled: u = !1
  } = e, {
    hasPopup: d = !1
  } = e, {
    color: h = "var(--block-label-text-color)"
  } = e, {
    transparent: p = !1
  } = e, {
    background: y = "var(--background-fill-primary)"
  } = e, {
    offset: L = 0
  } = e;
  function E(g) {
    lf.call(this, n, g);
  }
  return n.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, o = g.label), "show_label" in g && t(2, s = g.show_label), "pending" in g && t(3, f = g.pending), "size" in g && t(4, r = g.size), "padded" in g && t(5, a = g.padded), "highlight" in g && t(6, c = g.highlight), "disabled" in g && t(7, u = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, h = g.color), "transparent" in g && t(9, p = g.transparent), "background" in g && t(10, y = g.background), "offset" in g && t(11, L = g.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = c ? "var(--color-accent)" : h);
  }, [i, o, s, f, r, a, c, u, d, p, y, L, l, h, E];
}
class pf extends nf {
  constructor(e) {
    super(), rf(this, e, bf, gf, cf, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: wf,
  append: al,
  attr: Oe,
  detach: kf,
  init: vf,
  insert: Ef,
  noop: rl,
  safe_not_equal: Tf,
  set_style: Ge,
  svg_element: kn
} = window.__gradio__svelte__internal;
function yf(n) {
  let e, t, l, i;
  return {
    c() {
      e = kn("svg"), t = kn("g"), l = kn("path"), i = kn("path"), Oe(l, "d", "M18,6L6.087,17.913"), Ge(l, "fill", "none"), Ge(l, "fill-rule", "nonzero"), Ge(l, "stroke-width", "2px"), Oe(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Oe(i, "d", "M4.364,4.364L19.636,19.636"), Ge(i, "fill", "none"), Ge(i, "fill-rule", "nonzero"), Ge(i, "stroke-width", "2px"), Oe(e, "width", "100%"), Oe(e, "height", "100%"), Oe(e, "viewBox", "0 0 24 24"), Oe(e, "version", "1.1"), Oe(e, "xmlns", "http://www.w3.org/2000/svg"), Oe(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Oe(e, "xml:space", "preserve"), Oe(e, "stroke", "currentColor"), Ge(e, "fill-rule", "evenodd"), Ge(e, "clip-rule", "evenodd"), Ge(e, "stroke-linecap", "round"), Ge(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      Ef(o, e, s), al(e, t), al(t, l), al(e, i);
    },
    p: rl,
    i: rl,
    o: rl,
    d(o) {
      o && kf(e);
    }
  };
}
class Af extends wf {
  constructor(e) {
    super(), vf(this, e, null, yf, Tf, {});
  }
}
const {
  SvelteComponent: Sf,
  append: ht,
  attr: Fe,
  binding_callbacks: Ei,
  check_outros: Cl,
  create_component: Po,
  create_slot: Fo,
  destroy_component: Uo,
  destroy_each: zo,
  detach: D,
  element: Ye,
  empty: Pt,
  ensure_array_like: Ln,
  get_all_dirty_from_scope: qo,
  get_slot_changes: Ho,
  group_outros: Ll,
  init: Cf,
  insert: O,
  mount_component: Bo,
  noop: Rl,
  safe_not_equal: Lf,
  set_data: Se,
  set_style: _t,
  space: Ae,
  text: X,
  toggle_class: Te,
  transition_in: Pe,
  transition_out: Xe,
  update_slot_base: jo
} = window.__gradio__svelte__internal, {
  tick: Rf
} = window.__gradio__svelte__internal, {
  onDestroy: If
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Df
} = window.__gradio__svelte__internal, Of = (n) => ({}), Ti = (n) => ({}), Nf = (n) => ({}), yi = (n) => ({});
function Ai(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l[42] = t, l;
}
function Si(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l;
}
function Mf(n) {
  let e, t, l, i, o = (
    /*i18n*/
    n[1]("common.error") + ""
  ), s, f, r;
  t = new pf({
    props: {
      Icon: Af,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const a = (
    /*#slots*/
    n[30].error
  ), c = Fo(
    a,
    n,
    /*$$scope*/
    n[29],
    Ti
  );
  return {
    c() {
      e = Ye("div"), Po(t.$$.fragment), l = Ae(), i = Ye("span"), s = X(o), f = Ae(), c && c.c(), Fe(e, "class", "clear-status svelte-v0wucf"), Fe(i, "class", "error svelte-v0wucf");
    },
    m(u, d) {
      O(u, e, d), Bo(t, e, null), O(u, l, d), O(u, i, d), ht(i, s), O(u, f, d), c && c.m(u, d), r = !0;
    },
    p(u, d) {
      const h = {};
      d[0] & /*i18n*/
      2 && (h.label = /*i18n*/
      u[1]("common.clear")), t.$set(h), (!r || d[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      u[1]("common.error") + "") && Se(s, o), c && c.p && (!r || d[0] & /*$$scope*/
      536870912) && jo(
        c,
        a,
        u,
        /*$$scope*/
        u[29],
        r ? Ho(
          a,
          /*$$scope*/
          u[29],
          d,
          Of
        ) : qo(
          /*$$scope*/
          u[29]
        ),
        Ti
      );
    },
    i(u) {
      r || (Pe(t.$$.fragment, u), Pe(c, u), r = !0);
    },
    o(u) {
      Xe(t.$$.fragment, u), Xe(c, u), r = !1;
    },
    d(u) {
      u && (D(e), D(l), D(i), D(f)), Uo(t), c && c.d(u);
    }
  };
}
function Pf(n) {
  let e, t, l, i, o, s, f, r, a, c = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Ci(n)
  );
  function u(v, b) {
    if (
      /*progress*/
      v[7]
    ) return zf;
    if (
      /*queue_position*/
      v[2] !== null && /*queue_size*/
      v[3] !== void 0 && /*queue_position*/
      v[2] >= 0
    ) return Uf;
    if (
      /*queue_position*/
      v[2] === 0
    ) return Ff;
  }
  let d = u(n), h = d && d(n), p = (
    /*timer*/
    n[5] && Ii(n)
  );
  const y = [jf, Bf], L = [];
  function E(v, b) {
    return (
      /*last_progress_level*/
      v[15] != null ? 0 : (
        /*show_progress*/
        v[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = E(n)) && (s = L[o] = y[o](n));
  let g = !/*timer*/
  n[5] && Ui(n);
  return {
    c() {
      c && c.c(), e = Ae(), t = Ye("div"), h && h.c(), l = Ae(), p && p.c(), i = Ae(), s && s.c(), f = Ae(), g && g.c(), r = Pt(), Fe(t, "class", "progress-text svelte-v0wucf"), Te(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), Te(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(v, b) {
      c && c.m(v, b), O(v, e, b), O(v, t, b), h && h.m(t, null), ht(t, l), p && p.m(t, null), O(v, i, b), ~o && L[o].m(v, b), O(v, f, b), g && g.m(v, b), O(v, r, b), a = !0;
    },
    p(v, b) {
      /*variant*/
      v[8] === "default" && /*show_eta_bar*/
      v[18] && /*show_progress*/
      v[6] === "full" ? c ? c.p(v, b) : (c = Ci(v), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), d === (d = u(v)) && h ? h.p(v, b) : (h && h.d(1), h = d && d(v), h && (h.c(), h.m(t, l))), /*timer*/
      v[5] ? p ? p.p(v, b) : (p = Ii(v), p.c(), p.m(t, null)) : p && (p.d(1), p = null), (!a || b[0] & /*variant*/
      256) && Te(
        t,
        "meta-text-center",
        /*variant*/
        v[8] === "center"
      ), (!a || b[0] & /*variant*/
      256) && Te(
        t,
        "meta-text",
        /*variant*/
        v[8] === "default"
      );
      let S = o;
      o = E(v), o === S ? ~o && L[o].p(v, b) : (s && (Ll(), Xe(L[S], 1, 1, () => {
        L[S] = null;
      }), Cl()), ~o ? (s = L[o], s ? s.p(v, b) : (s = L[o] = y[o](v), s.c()), Pe(s, 1), s.m(f.parentNode, f)) : s = null), /*timer*/
      v[5] ? g && (Ll(), Xe(g, 1, 1, () => {
        g = null;
      }), Cl()) : g ? (g.p(v, b), b[0] & /*timer*/
      32 && Pe(g, 1)) : (g = Ui(v), g.c(), Pe(g, 1), g.m(r.parentNode, r));
    },
    i(v) {
      a || (Pe(s), Pe(g), a = !0);
    },
    o(v) {
      Xe(s), Xe(g), a = !1;
    },
    d(v) {
      v && (D(e), D(t), D(i), D(f), D(r)), c && c.d(v), h && h.d(), p && p.d(), ~o && L[o].d(v), g && g.d(v);
    }
  };
}
function Ci(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Ye("div"), Fe(e, "class", "eta-bar svelte-v0wucf"), _t(e, "transform", t);
    },
    m(l, i) {
      O(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && _t(e, "transform", t);
    },
    d(l) {
      l && D(e);
    }
  };
}
function Ff(n) {
  let e;
  return {
    c() {
      e = X("processing |");
    },
    m(t, l) {
      O(t, e, l);
    },
    p: Rl,
    d(t) {
      t && D(e);
    }
  };
}
function Uf(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, o, s;
  return {
    c() {
      e = X("queue: "), l = X(t), i = X("/"), o = X(
        /*queue_size*/
        n[3]
      ), s = X(" |");
    },
    m(f, r) {
      O(f, e, r), O(f, l, r), O(f, i, r), O(f, o, r), O(f, s, r);
    },
    p(f, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && Se(l, t), r[0] & /*queue_size*/
      8 && Se(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (D(e), D(l), D(i), D(o), D(s));
    }
  };
}
function zf(n) {
  let e, t = Ln(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Ri(Si(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = Pt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      O(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Ln(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Si(i, t, s);
          l[s] ? l[s].p(f, o) : (l[s] = Ri(f), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && D(e), zo(l, i);
    }
  };
}
function Li(n) {
  let e, t = (
    /*p*/
    n[40].unit + ""
  ), l, i, o = " ", s;
  function f(c, u) {
    return (
      /*p*/
      c[40].length != null ? Hf : qf
    );
  }
  let r = f(n), a = r(n);
  return {
    c() {
      a.c(), e = Ae(), l = X(t), i = X(" | "), s = X(o);
    },
    m(c, u) {
      a.m(c, u), O(c, e, u), O(c, l, u), O(c, i, u), O(c, s, u);
    },
    p(c, u) {
      r === (r = f(c)) && a ? a.p(c, u) : (a.d(1), a = r(c), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[40].unit + "") && Se(l, t);
    },
    d(c) {
      c && (D(e), D(l), D(i), D(s)), a.d(c);
    }
  };
}
function qf(n) {
  let e = Dt(
    /*p*/
    n[40].index || 0
  ) + "", t;
  return {
    c() {
      t = X(e);
    },
    m(l, i) {
      O(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = Dt(
        /*p*/
        l[40].index || 0
      ) + "") && Se(t, e);
    },
    d(l) {
      l && D(t);
    }
  };
}
function Hf(n) {
  let e = Dt(
    /*p*/
    n[40].index || 0
  ) + "", t, l, i = Dt(
    /*p*/
    n[40].length
  ) + "", o;
  return {
    c() {
      t = X(e), l = X("/"), o = X(i);
    },
    m(s, f) {
      O(s, t, f), O(s, l, f), O(s, o, f);
    },
    p(s, f) {
      f[0] & /*progress*/
      128 && e !== (e = Dt(
        /*p*/
        s[40].index || 0
      ) + "") && Se(t, e), f[0] & /*progress*/
      128 && i !== (i = Dt(
        /*p*/
        s[40].length
      ) + "") && Se(o, i);
    },
    d(s) {
      s && (D(t), D(l), D(o));
    }
  };
}
function Ri(n) {
  let e, t = (
    /*p*/
    n[40].index != null && Li(n)
  );
  return {
    c() {
      t && t.c(), e = Pt();
    },
    m(l, i) {
      t && t.m(l, i), O(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].index != null ? t ? t.p(l, i) : (t = Li(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && D(e), t && t.d(l);
    }
  };
}
function Ii(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = X(
        /*formatted_timer*/
        n[20]
      ), l = X(t), i = X("s");
    },
    m(o, s) {
      O(o, e, s), O(o, l, s), O(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && Se(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && Se(l, t);
    },
    d(o) {
      o && (D(e), D(l), D(i));
    }
  };
}
function Bf(n) {
  let e, t;
  return e = new Oo({
    props: {
      margin: (
        /*variant*/
        n[8] === "default"
      )
    }
  }), {
    c() {
      Po(e.$$.fragment);
    },
    m(l, i) {
      Bo(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      l[8] === "default"), e.$set(o);
    },
    i(l) {
      t || (Pe(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Xe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Uo(e, l);
    }
  };
}
function jf(n) {
  let e, t, l, i, o, s = `${/*last_progress_level*/
  n[15] * 100}%`, f = (
    /*progress*/
    n[7] != null && Di(n)
  );
  return {
    c() {
      e = Ye("div"), t = Ye("div"), f && f.c(), l = Ae(), i = Ye("div"), o = Ye("div"), Fe(t, "class", "progress-level-inner svelte-v0wucf"), Fe(o, "class", "progress-bar svelte-v0wucf"), _t(o, "width", s), Fe(i, "class", "progress-bar-wrap svelte-v0wucf"), Fe(e, "class", "progress-level svelte-v0wucf");
    },
    m(r, a) {
      O(r, e, a), ht(e, t), f && f.m(t, null), ht(e, l), ht(e, i), ht(i, o), n[31](o);
    },
    p(r, a) {
      /*progress*/
      r[7] != null ? f ? f.p(r, a) : (f = Di(r), f.c(), f.m(t, null)) : f && (f.d(1), f = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      r[15] * 100}%`) && _t(o, "width", s);
    },
    i: Rl,
    o: Rl,
    d(r) {
      r && D(e), f && f.d(), n[31](null);
    }
  };
}
function Di(n) {
  let e, t = Ln(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Fi(Ai(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = Pt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      O(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Ln(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Ai(i, t, s);
          l[s] ? l[s].p(f, o) : (l[s] = Fi(f), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && D(e), zo(l, i);
    }
  };
}
function Oi(n) {
  let e, t, l, i, o = (
    /*i*/
    n[42] !== 0 && Wf()
  ), s = (
    /*p*/
    n[40].desc != null && Ni(n)
  ), f = (
    /*p*/
    n[40].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null && Mi()
  ), r = (
    /*progress_level*/
    n[14] != null && Pi(n)
  );
  return {
    c() {
      o && o.c(), e = Ae(), s && s.c(), t = Ae(), f && f.c(), l = Ae(), r && r.c(), i = Pt();
    },
    m(a, c) {
      o && o.m(a, c), O(a, e, c), s && s.m(a, c), O(a, t, c), f && f.m(a, c), O(a, l, c), r && r.m(a, c), O(a, i, c);
    },
    p(a, c) {
      /*p*/
      a[40].desc != null ? s ? s.p(a, c) : (s = Ni(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[40].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[42]
      ] != null ? f || (f = Mi(), f.c(), f.m(l.parentNode, l)) : f && (f.d(1), f = null), /*progress_level*/
      a[14] != null ? r ? r.p(a, c) : (r = Pi(a), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(a) {
      a && (D(e), D(t), D(l), D(i)), o && o.d(a), s && s.d(a), f && f.d(a), r && r.d(a);
    }
  };
}
function Wf(n) {
  let e;
  return {
    c() {
      e = X(" /");
    },
    m(t, l) {
      O(t, e, l);
    },
    d(t) {
      t && D(e);
    }
  };
}
function Ni(n) {
  let e = (
    /*p*/
    n[40].desc + ""
  ), t;
  return {
    c() {
      t = X(e);
    },
    m(l, i) {
      O(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[40].desc + "") && Se(t, e);
    },
    d(l) {
      l && D(t);
    }
  };
}
function Mi(n) {
  let e;
  return {
    c() {
      e = X("-");
    },
    m(t, l) {
      O(t, e, l);
    },
    d(t) {
      t && D(e);
    }
  };
}
function Pi(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[42]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = X(e), l = X("%");
    },
    m(i, o) {
      O(i, t, o), O(i, l, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[42]
      ] || 0)).toFixed(1) + "") && Se(t, e);
    },
    d(i) {
      i && (D(t), D(l));
    }
  };
}
function Fi(n) {
  let e, t = (
    /*p*/
    (n[40].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null) && Oi(n)
  );
  return {
    c() {
      t && t.c(), e = Pt();
    },
    m(l, i) {
      t && t.m(l, i), O(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[42]
      ] != null ? t ? t.p(l, i) : (t = Oi(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && D(e), t && t.d(l);
    }
  };
}
function Ui(n) {
  let e, t, l, i;
  const o = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), s = Fo(
    o,
    n,
    /*$$scope*/
    n[29],
    yi
  );
  return {
    c() {
      e = Ye("p"), t = X(
        /*loading_text*/
        n[9]
      ), l = Ae(), s && s.c(), Fe(e, "class", "loading svelte-v0wucf");
    },
    m(f, r) {
      O(f, e, r), ht(e, t), O(f, l, r), s && s.m(f, r), i = !0;
    },
    p(f, r) {
      (!i || r[0] & /*loading_text*/
      512) && Se(
        t,
        /*loading_text*/
        f[9]
      ), s && s.p && (!i || r[0] & /*$$scope*/
      536870912) && jo(
        s,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Ho(
          o,
          /*$$scope*/
          f[29],
          r,
          Nf
        ) : qo(
          /*$$scope*/
          f[29]
        ),
        yi
      );
    },
    i(f) {
      i || (Pe(s, f), i = !0);
    },
    o(f) {
      Xe(s, f), i = !1;
    },
    d(f) {
      f && (D(e), D(l)), s && s.d(f);
    }
  };
}
function Gf(n) {
  let e, t, l, i, o;
  const s = [Pf, Mf], f = [];
  function r(a, c) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(n)) && (l = f[t] = s[t](n)), {
    c() {
      e = Ye("div"), l && l.c(), Fe(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-v0wucf"), Te(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), Te(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), Te(
        e,
        "generating",
        /*status*/
        n[4] === "generating" && /*show_progress*/
        n[6] === "full"
      ), Te(
        e,
        "border",
        /*border*/
        n[12]
      ), _t(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), _t(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, c) {
      O(a, e, c), ~t && f[t].m(e, null), n[33](e), o = !0;
    },
    p(a, c) {
      let u = t;
      t = r(a), t === u ? ~t && f[t].p(a, c) : (l && (Ll(), Xe(f[u], 1, 1, () => {
        f[u] = null;
      }), Cl()), ~t ? (l = f[t], l ? l.p(a, c) : (l = f[t] = s[t](a), l.c()), Pe(l, 1), l.m(e, null)) : l = null), (!o || c[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-v0wucf")) && Fe(e, "class", i), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && Te(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!o || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Te(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && Te(
        e,
        "generating",
        /*status*/
        a[4] === "generating" && /*show_progress*/
        a[6] === "full"
      ), (!o || c[0] & /*variant, show_progress, border*/
      4416) && Te(
        e,
        "border",
        /*border*/
        a[12]
      ), c[0] & /*absolute*/
      1024 && _t(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && _t(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      o || (Pe(l), o = !0);
    },
    o(a) {
      Xe(l), o = !1;
    },
    d(a) {
      a && D(e), ~t && f[t].d(), n[33](null);
    }
  };
}
let vn = [], sl = !1;
async function Vf(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (vn.push(n), !sl) sl = !0;
    else return;
    await Rf(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < vn.length; l++) {
        const o = vn[l].getBoundingClientRect();
        (l === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({
        top: t[0] - 20,
        behavior: "smooth"
      }), sl = !1, vn = [];
    });
  }
}
function Yf(n, e, t) {
  let l, {
    $$slots: i = {},
    $$scope: o
  } = e;
  const s = Df();
  let {
    i18n: f
  } = e, {
    eta: r = null
  } = e, {
    queue_position: a
  } = e, {
    queue_size: c
  } = e, {
    status: u
  } = e, {
    scroll_to_output: d = !1
  } = e, {
    timer: h = !0
  } = e, {
    show_progress: p = "full"
  } = e, {
    message: y = null
  } = e, {
    progress: L = null
  } = e, {
    variant: E = "default"
  } = e, {
    loading_text: g = "Loading..."
  } = e, {
    absolute: v = !0
  } = e, {
    translucent: b = !1
  } = e, {
    border: S = !1
  } = e, {
    autoscroll: w
  } = e, I, A = !1, Z = 0, z = 0, F = null, H = null, ce = 0, J = null, ke, x = null, be = !0;
  const ve = () => {
    t(0, r = t(27, F = t(19, U = null))), t(25, Z = performance.now()), t(26, z = 0), A = !0, ie();
  };
  function ie() {
    requestAnimationFrame(() => {
      t(26, z = (performance.now() - Z) / 1e3), A && ie();
    });
  }
  function G() {
    t(26, z = 0), t(0, r = t(27, F = t(19, U = null))), A && (A = !1);
  }
  If(() => {
    A && G();
  });
  let U = null;
  function qe(m) {
    Ei[m ? "unshift" : "push"](() => {
      x = m, t(16, x), t(7, L), t(14, J), t(15, ke);
    });
  }
  const W = () => {
    s("clear_status");
  };
  function ot(m) {
    Ei[m ? "unshift" : "push"](() => {
      I = m, t(13, I);
    });
  }
  return n.$$set = (m) => {
    "i18n" in m && t(1, f = m.i18n), "eta" in m && t(0, r = m.eta), "queue_position" in m && t(2, a = m.queue_position), "queue_size" in m && t(3, c = m.queue_size), "status" in m && t(4, u = m.status), "scroll_to_output" in m && t(22, d = m.scroll_to_output), "timer" in m && t(5, h = m.timer), "show_progress" in m && t(6, p = m.show_progress), "message" in m && t(23, y = m.message), "progress" in m && t(7, L = m.progress), "variant" in m && t(8, E = m.variant), "loading_text" in m && t(9, g = m.loading_text), "absolute" in m && t(10, v = m.absolute), "translucent" in m && t(11, b = m.translucent), "border" in m && t(12, S = m.border), "autoscroll" in m && t(24, w = m.autoscroll), "$$scope" in m && t(29, o = m.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (r === null && t(0, r = F), r != null && F !== r && (t(28, H = (performance.now() - Z) / 1e3 + r), t(19, U = H.toFixed(1)), t(27, F = r))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ce = H === null || H <= 0 || !z ? null : Math.min(z / H, 1)), n.$$.dirty[0] & /*progress*/
    128 && L != null && t(18, be = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (L != null ? t(14, J = L.map((m) => {
      if (m.index != null && m.length != null)
        return m.index / m.length;
      if (m.progress != null)
        return m.progress;
    })) : t(14, J = null), J ? (t(15, ke = J[J.length - 1]), x && (ke === 0 ? t(16, x.style.transition = "0", x) : t(16, x.style.transition = "150ms", x))) : t(15, ke = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? ve() : G()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && I && d && (u === "pending" || u === "complete") && Vf(I, w), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = z.toFixed(1));
  }, [r, f, a, c, u, h, p, L, E, g, v, b, S, I, J, ke, x, ce, be, U, l, s, d, y, w, Z, z, F, H, o, i, qe, W, ot];
}
class Xf extends Sf {
  constructor(e) {
    super(), Cf(this, e, Yf, Gf, Lf, {
      i18n: 1,
      eta: 0,
      queue_position: 2,
      queue_size: 3,
      status: 4,
      scroll_to_output: 22,
      timer: 5,
      show_progress: 6,
      message: 23,
      progress: 7,
      variant: 8,
      loading_text: 9,
      absolute: 10,
      translucent: 11,
      border: 12,
      autoscroll: 24
    }, null, [-1, -1]);
  }
}
/*! @license DOMPurify 3.1.6 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.1.6/LICENSE */
const {
  entries: Wo,
  setPrototypeOf: zi,
  isFrozen: Zf,
  getPrototypeOf: Kf,
  getOwnPropertyDescriptor: Jf
} = Object;
let {
  freeze: fe,
  seal: Ce,
  create: Go
} = Object, {
  apply: Il,
  construct: Dl
} = typeof Reflect < "u" && Reflect;
fe || (fe = function(e) {
  return e;
});
Ce || (Ce = function(e) {
  return e;
});
Il || (Il = function(e, t, l) {
  return e.apply(t, l);
});
Dl || (Dl = function(e, t) {
  return new e(...t);
});
const En = we(Array.prototype.forEach), qi = we(Array.prototype.pop), Xt = we(Array.prototype.push), Sn = we(String.prototype.toLowerCase), fl = we(String.prototype.toString), Hi = we(String.prototype.match), Zt = we(String.prototype.replace), Qf = we(String.prototype.indexOf), xf = we(String.prototype.trim), Ne = we(Object.prototype.hasOwnProperty), re = we(RegExp.prototype.test), Kt = $f(TypeError);
function we(n) {
  return function(e) {
    for (var t = arguments.length, l = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
      l[i - 1] = arguments[i];
    return Il(n, e, l);
  };
}
function $f(n) {
  return function() {
    for (var e = arguments.length, t = new Array(e), l = 0; l < e; l++)
      t[l] = arguments[l];
    return Dl(n, t);
  };
}
function N(n, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : Sn;
  zi && zi(n, null);
  let l = e.length;
  for (; l--; ) {
    let i = e[l];
    if (typeof i == "string") {
      const o = t(i);
      o !== i && (Zf(e) || (e[l] = o), i = o);
    }
    n[i] = !0;
  }
  return n;
}
function ec(n) {
  for (let e = 0; e < n.length; e++)
    Ne(n, e) || (n[e] = null);
  return n;
}
function mt(n) {
  const e = Go(null);
  for (const [t, l] of Wo(n))
    Ne(n, t) && (Array.isArray(l) ? e[t] = ec(l) : l && typeof l == "object" && l.constructor === Object ? e[t] = mt(l) : e[t] = l);
  return e;
}
function Jt(n, e) {
  for (; n !== null; ) {
    const l = Jf(n, e);
    if (l) {
      if (l.get)
        return we(l.get);
      if (typeof l.value == "function")
        return we(l.value);
    }
    n = Kf(n);
  }
  function t() {
    return null;
  }
  return t;
}
const Bi = fe(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), cl = fe(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), ul = fe(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), tc = fe(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), _l = fe(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), nc = fe(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), ji = fe(["#text"]), Wi = fe(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), dl = fe(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), Gi = fe(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Tn = fe(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), lc = Ce(/\{\{[\w\W]*|[\w\W]*\}\}/gm), ic = Ce(/<%[\w\W]*|[\w\W]*%>/gm), oc = Ce(/\${[\w\W]*}/gm), ac = Ce(/^data-[\-\w.\u00B7-\uFFFF]/), rc = Ce(/^aria-[\-\w]+$/), Vo = Ce(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), sc = Ce(/^(?:\w+script|data):/i), fc = Ce(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), Yo = Ce(/^html$/i), cc = Ce(/^[a-z][.\w]*(-[.\w]+)+$/i);
var Vi = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR: lc,
  ERB_EXPR: ic,
  TMPLIT_EXPR: oc,
  DATA_ATTR: ac,
  ARIA_ATTR: rc,
  IS_ALLOWED_URI: Vo,
  IS_SCRIPT_OR_DATA: sc,
  ATTR_WHITESPACE: fc,
  DOCTYPE_NAME: Yo,
  CUSTOM_ELEMENT: cc
});
const Qt = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, uc = function() {
  return typeof window > "u" ? null : window;
}, _c = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let l = null;
  const i = "data-tt-policy-suffix";
  t && t.hasAttribute(i) && (l = t.getAttribute(i));
  const o = "dompurify" + (l ? "#" + l : "");
  try {
    return e.createPolicy(o, {
      createHTML(s) {
        return s;
      },
      createScriptURL(s) {
        return s;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function Xo() {
  let n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : uc();
  const e = (R) => Xo(R);
  if (e.version = "3.1.6", e.removed = [], !n || !n.document || n.document.nodeType !== Qt.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = n;
  const l = t, i = l.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: s,
    Node: f,
    Element: r,
    NodeFilter: a,
    NamedNodeMap: c = n.NamedNodeMap || n.MozNamedAttrMap,
    HTMLFormElement: u,
    DOMParser: d,
    trustedTypes: h
  } = n, p = r.prototype, y = Jt(p, "cloneNode"), L = Jt(p, "remove"), E = Jt(p, "nextSibling"), g = Jt(p, "childNodes"), v = Jt(p, "parentNode");
  if (typeof s == "function") {
    const R = t.createElement("template");
    R.content && R.content.ownerDocument && (t = R.content.ownerDocument);
  }
  let b, S = "";
  const {
    implementation: w,
    createNodeIterator: I,
    createDocumentFragment: A,
    getElementsByTagName: Z
  } = t, {
    importNode: z
  } = l;
  let F = {};
  e.isSupported = typeof Wo == "function" && typeof v == "function" && w && w.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: H,
    ERB_EXPR: ce,
    TMPLIT_EXPR: J,
    DATA_ATTR: ke,
    ARIA_ATTR: x,
    IS_SCRIPT_OR_DATA: be,
    ATTR_WHITESPACE: ve,
    CUSTOM_ELEMENT: ie
  } = Vi;
  let {
    IS_ALLOWED_URI: G
  } = Vi, U = null;
  const qe = N({}, [...Bi, ...cl, ...ul, ..._l, ...ji]);
  let W = null;
  const ot = N({}, [...Wi, ...dl, ...Gi, ...Tn]);
  let m = Object.seal(Go(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), ue = null, Ft = null, sn = !0, Ut = !0, fn = !1, cn = !0, at = !1, zt = !0, Ke = !1, qt = !1, Ht = !1, rt = !1, vt = !1, Et = !1, un = !0, _n = !1;
  const Wn = "user-content-";
  let Bt = !0, k = !1, B = {}, $ = null;
  const jt = N({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let Tt = null;
  const Gn = N({}, ["audio", "video", "img", "source", "image", "track"]);
  let yt = null;
  const Wt = N({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), dn = "http://www.w3.org/1998/Math/MathML", mn = "http://www.w3.org/2000/svg", Je = "http://www.w3.org/1999/xhtml";
  let At = Je, Vn = !1, Yn = null;
  const ha = N({}, [dn, mn, Je], fl);
  let Gt = null;
  const ga = ["application/xhtml+xml", "text/html"], ba = "text/html";
  let Q = null, St = null;
  const pa = t.createElement("form"), jl = function(_) {
    return _ instanceof RegExp || _ instanceof Function;
  }, Xn = function() {
    let _ = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(St && St === _)) {
      if ((!_ || typeof _ != "object") && (_ = {}), _ = mt(_), Gt = // eslint-disable-next-line unicorn/prefer-includes
      ga.indexOf(_.PARSER_MEDIA_TYPE) === -1 ? ba : _.PARSER_MEDIA_TYPE, Q = Gt === "application/xhtml+xml" ? fl : Sn, U = Ne(_, "ALLOWED_TAGS") ? N({}, _.ALLOWED_TAGS, Q) : qe, W = Ne(_, "ALLOWED_ATTR") ? N({}, _.ALLOWED_ATTR, Q) : ot, Yn = Ne(_, "ALLOWED_NAMESPACES") ? N({}, _.ALLOWED_NAMESPACES, fl) : ha, yt = Ne(_, "ADD_URI_SAFE_ATTR") ? N(
        mt(Wt),
        // eslint-disable-line indent
        _.ADD_URI_SAFE_ATTR,
        // eslint-disable-line indent
        Q
        // eslint-disable-line indent
      ) : Wt, Tt = Ne(_, "ADD_DATA_URI_TAGS") ? N(
        mt(Gn),
        // eslint-disable-line indent
        _.ADD_DATA_URI_TAGS,
        // eslint-disable-line indent
        Q
        // eslint-disable-line indent
      ) : Gn, $ = Ne(_, "FORBID_CONTENTS") ? N({}, _.FORBID_CONTENTS, Q) : jt, ue = Ne(_, "FORBID_TAGS") ? N({}, _.FORBID_TAGS, Q) : {}, Ft = Ne(_, "FORBID_ATTR") ? N({}, _.FORBID_ATTR, Q) : {}, B = Ne(_, "USE_PROFILES") ? _.USE_PROFILES : !1, sn = _.ALLOW_ARIA_ATTR !== !1, Ut = _.ALLOW_DATA_ATTR !== !1, fn = _.ALLOW_UNKNOWN_PROTOCOLS || !1, cn = _.ALLOW_SELF_CLOSE_IN_ATTR !== !1, at = _.SAFE_FOR_TEMPLATES || !1, zt = _.SAFE_FOR_XML !== !1, Ke = _.WHOLE_DOCUMENT || !1, rt = _.RETURN_DOM || !1, vt = _.RETURN_DOM_FRAGMENT || !1, Et = _.RETURN_TRUSTED_TYPE || !1, Ht = _.FORCE_BODY || !1, un = _.SANITIZE_DOM !== !1, _n = _.SANITIZE_NAMED_PROPS || !1, Bt = _.KEEP_CONTENT !== !1, k = _.IN_PLACE || !1, G = _.ALLOWED_URI_REGEXP || Vo, At = _.NAMESPACE || Je, m = _.CUSTOM_ELEMENT_HANDLING || {}, _.CUSTOM_ELEMENT_HANDLING && jl(_.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (m.tagNameCheck = _.CUSTOM_ELEMENT_HANDLING.tagNameCheck), _.CUSTOM_ELEMENT_HANDLING && jl(_.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (m.attributeNameCheck = _.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), _.CUSTOM_ELEMENT_HANDLING && typeof _.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (m.allowCustomizedBuiltInElements = _.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), at && (Ut = !1), vt && (rt = !0), B && (U = N({}, ji), W = [], B.html === !0 && (N(U, Bi), N(W, Wi)), B.svg === !0 && (N(U, cl), N(W, dl), N(W, Tn)), B.svgFilters === !0 && (N(U, ul), N(W, dl), N(W, Tn)), B.mathMl === !0 && (N(U, _l), N(W, Gi), N(W, Tn))), _.ADD_TAGS && (U === qe && (U = mt(U)), N(U, _.ADD_TAGS, Q)), _.ADD_ATTR && (W === ot && (W = mt(W)), N(W, _.ADD_ATTR, Q)), _.ADD_URI_SAFE_ATTR && N(yt, _.ADD_URI_SAFE_ATTR, Q), _.FORBID_CONTENTS && ($ === jt && ($ = mt($)), N($, _.FORBID_CONTENTS, Q)), Bt && (U["#text"] = !0), Ke && N(U, ["html", "head", "body"]), U.table && (N(U, ["tbody"]), delete ue.tbody), _.TRUSTED_TYPES_POLICY) {
        if (typeof _.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw Kt('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof _.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw Kt('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        b = _.TRUSTED_TYPES_POLICY, S = b.createHTML("");
      } else
        b === void 0 && (b = _c(h, i)), b !== null && typeof S == "string" && (S = b.createHTML(""));
      fe && fe(_), St = _;
    }
  }, Wl = N({}, ["mi", "mo", "mn", "ms", "mtext"]), Gl = N({}, ["foreignobject", "annotation-xml"]), wa = N({}, ["title", "style", "font", "a", "script"]), Vl = N({}, [...cl, ...ul, ...tc]), Yl = N({}, [..._l, ...nc]), ka = function(_) {
    let T = v(_);
    (!T || !T.tagName) && (T = {
      namespaceURI: At,
      tagName: "template"
    });
    const C = Sn(_.tagName), j = Sn(T.tagName);
    return Yn[_.namespaceURI] ? _.namespaceURI === mn ? T.namespaceURI === Je ? C === "svg" : T.namespaceURI === dn ? C === "svg" && (j === "annotation-xml" || Wl[j]) : !!Vl[C] : _.namespaceURI === dn ? T.namespaceURI === Je ? C === "math" : T.namespaceURI === mn ? C === "math" && Gl[j] : !!Yl[C] : _.namespaceURI === Je ? T.namespaceURI === mn && !Gl[j] || T.namespaceURI === dn && !Wl[j] ? !1 : !Yl[C] && (wa[C] || !Vl[C]) : !!(Gt === "application/xhtml+xml" && Yn[_.namespaceURI]) : !1;
  }, He = function(_) {
    Xt(e.removed, {
      element: _
    });
    try {
      v(_).removeChild(_);
    } catch {
      L(_);
    }
  }, hn = function(_, T) {
    try {
      Xt(e.removed, {
        attribute: T.getAttributeNode(_),
        from: T
      });
    } catch {
      Xt(e.removed, {
        attribute: null,
        from: T
      });
    }
    if (T.removeAttribute(_), _ === "is" && !W[_])
      if (rt || vt)
        try {
          He(T);
        } catch {
        }
      else
        try {
          T.setAttribute(_, "");
        } catch {
        }
  }, Xl = function(_) {
    let T = null, C = null;
    if (Ht)
      _ = "<remove></remove>" + _;
    else {
      const ee = Hi(_, /^[\r\n\t ]+/);
      C = ee && ee[0];
    }
    Gt === "application/xhtml+xml" && At === Je && (_ = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + _ + "</body></html>");
    const j = b ? b.createHTML(_) : _;
    if (At === Je)
      try {
        T = new d().parseFromString(j, Gt);
      } catch {
      }
    if (!T || !T.documentElement) {
      T = w.createDocument(At, "template", null);
      try {
        T.documentElement.innerHTML = Vn ? S : j;
      } catch {
      }
    }
    const ne = T.body || T.documentElement;
    return _ && C && ne.insertBefore(t.createTextNode(C), ne.childNodes[0] || null), At === Je ? Z.call(T, Ke ? "html" : "body")[0] : Ke ? T.documentElement : ne;
  }, Zl = function(_) {
    return I.call(
      _.ownerDocument || _,
      _,
      // eslint-disable-next-line no-bitwise
      a.SHOW_ELEMENT | a.SHOW_COMMENT | a.SHOW_TEXT | a.SHOW_PROCESSING_INSTRUCTION | a.SHOW_CDATA_SECTION,
      null
    );
  }, Kl = function(_) {
    return _ instanceof u && (typeof _.nodeName != "string" || typeof _.textContent != "string" || typeof _.removeChild != "function" || !(_.attributes instanceof c) || typeof _.removeAttribute != "function" || typeof _.setAttribute != "function" || typeof _.namespaceURI != "string" || typeof _.insertBefore != "function" || typeof _.hasChildNodes != "function");
  }, Jl = function(_) {
    return typeof f == "function" && _ instanceof f;
  }, Qe = function(_, T, C) {
    F[_] && En(F[_], (j) => {
      j.call(e, T, C, St);
    });
  }, Ql = function(_) {
    let T = null;
    if (Qe("beforeSanitizeElements", _, null), Kl(_))
      return He(_), !0;
    const C = Q(_.nodeName);
    if (Qe("uponSanitizeElement", _, {
      tagName: C,
      allowedTags: U
    }), _.hasChildNodes() && !Jl(_.firstElementChild) && re(/<[/\w]/g, _.innerHTML) && re(/<[/\w]/g, _.textContent) || _.nodeType === Qt.progressingInstruction || zt && _.nodeType === Qt.comment && re(/<[/\w]/g, _.data))
      return He(_), !0;
    if (!U[C] || ue[C]) {
      if (!ue[C] && $l(C) && (m.tagNameCheck instanceof RegExp && re(m.tagNameCheck, C) || m.tagNameCheck instanceof Function && m.tagNameCheck(C)))
        return !1;
      if (Bt && !$[C]) {
        const j = v(_) || _.parentNode, ne = g(_) || _.childNodes;
        if (ne && j) {
          const ee = ne.length;
          for (let _e = ee - 1; _e >= 0; --_e) {
            const Be = y(ne[_e], !0);
            Be.__removalCount = (_.__removalCount || 0) + 1, j.insertBefore(Be, E(_));
          }
        }
      }
      return He(_), !0;
    }
    return _ instanceof r && !ka(_) || (C === "noscript" || C === "noembed" || C === "noframes") && re(/<\/no(script|embed|frames)/i, _.innerHTML) ? (He(_), !0) : (at && _.nodeType === Qt.text && (T = _.textContent, En([H, ce, J], (j) => {
      T = Zt(T, j, " ");
    }), _.textContent !== T && (Xt(e.removed, {
      element: _.cloneNode()
    }), _.textContent = T)), Qe("afterSanitizeElements", _, null), !1);
  }, xl = function(_, T, C) {
    if (un && (T === "id" || T === "name") && (C in t || C in pa))
      return !1;
    if (!(Ut && !Ft[T] && re(ke, T))) {
      if (!(sn && re(x, T))) {
        if (!W[T] || Ft[T]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !($l(_) && (m.tagNameCheck instanceof RegExp && re(m.tagNameCheck, _) || m.tagNameCheck instanceof Function && m.tagNameCheck(_)) && (m.attributeNameCheck instanceof RegExp && re(m.attributeNameCheck, T) || m.attributeNameCheck instanceof Function && m.attributeNameCheck(T)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            T === "is" && m.allowCustomizedBuiltInElements && (m.tagNameCheck instanceof RegExp && re(m.tagNameCheck, C) || m.tagNameCheck instanceof Function && m.tagNameCheck(C)))
          ) return !1;
        } else if (!yt[T]) {
          if (!re(G, Zt(C, ve, ""))) {
            if (!((T === "src" || T === "xlink:href" || T === "href") && _ !== "script" && Qf(C, "data:") === 0 && Tt[_])) {
              if (!(fn && !re(be, Zt(C, ve, "")))) {
                if (C)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, $l = function(_) {
    return _ !== "annotation-xml" && Hi(_, ie);
  }, ei = function(_) {
    Qe("beforeSanitizeAttributes", _, null);
    const {
      attributes: T
    } = _;
    if (!T)
      return;
    const C = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: W
    };
    let j = T.length;
    for (; j--; ) {
      const ne = T[j], {
        name: ee,
        namespaceURI: _e,
        value: Be
      } = ne, Vt = Q(ee);
      let oe = ee === "value" ? Be : xf(Be);
      if (C.attrName = Vt, C.attrValue = oe, C.keepAttr = !0, C.forceKeepAttr = void 0, Qe("uponSanitizeAttribute", _, C), oe = C.attrValue, zt && re(/((--!?|])>)|<\/(style|title)/i, oe)) {
        hn(ee, _);
        continue;
      }
      if (C.forceKeepAttr || (hn(ee, _), !C.keepAttr))
        continue;
      if (!cn && re(/\/>/i, oe)) {
        hn(ee, _);
        continue;
      }
      at && En([H, ce, J], (ni) => {
        oe = Zt(oe, ni, " ");
      });
      const ti = Q(_.nodeName);
      if (xl(ti, Vt, oe)) {
        if (_n && (Vt === "id" || Vt === "name") && (hn(ee, _), oe = Wn + oe), b && typeof h == "object" && typeof h.getAttributeType == "function" && !_e)
          switch (h.getAttributeType(ti, Vt)) {
            case "TrustedHTML": {
              oe = b.createHTML(oe);
              break;
            }
            case "TrustedScriptURL": {
              oe = b.createScriptURL(oe);
              break;
            }
          }
        try {
          _e ? _.setAttributeNS(_e, ee, oe) : _.setAttribute(ee, oe), Kl(_) ? He(_) : qi(e.removed);
        } catch {
        }
      }
    }
    Qe("afterSanitizeAttributes", _, null);
  }, va = function R(_) {
    let T = null;
    const C = Zl(_);
    for (Qe("beforeSanitizeShadowDOM", _, null); T = C.nextNode(); )
      Qe("uponSanitizeShadowNode", T, null), !Ql(T) && (T.content instanceof o && R(T.content), ei(T));
    Qe("afterSanitizeShadowDOM", _, null);
  };
  return e.sanitize = function(R) {
    let _ = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, T = null, C = null, j = null, ne = null;
    if (Vn = !R, Vn && (R = "<!-->"), typeof R != "string" && !Jl(R))
      if (typeof R.toString == "function") {
        if (R = R.toString(), typeof R != "string")
          throw Kt("dirty is not a string, aborting");
      } else
        throw Kt("toString is not a function");
    if (!e.isSupported)
      return R;
    if (qt || Xn(_), e.removed = [], typeof R == "string" && (k = !1), k) {
      if (R.nodeName) {
        const Be = Q(R.nodeName);
        if (!U[Be] || ue[Be])
          throw Kt("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (R instanceof f)
      T = Xl("<!---->"), C = T.ownerDocument.importNode(R, !0), C.nodeType === Qt.element && C.nodeName === "BODY" || C.nodeName === "HTML" ? T = C : T.appendChild(C);
    else {
      if (!rt && !at && !Ke && // eslint-disable-next-line unicorn/prefer-includes
      R.indexOf("<") === -1)
        return b && Et ? b.createHTML(R) : R;
      if (T = Xl(R), !T)
        return rt ? null : Et ? S : "";
    }
    T && Ht && He(T.firstChild);
    const ee = Zl(k ? R : T);
    for (; j = ee.nextNode(); )
      Ql(j) || (j.content instanceof o && va(j.content), ei(j));
    if (k)
      return R;
    if (rt) {
      if (vt)
        for (ne = A.call(T.ownerDocument); T.firstChild; )
          ne.appendChild(T.firstChild);
      else
        ne = T;
      return (W.shadowroot || W.shadowrootmode) && (ne = z.call(l, ne, !0)), ne;
    }
    let _e = Ke ? T.outerHTML : T.innerHTML;
    return Ke && U["!doctype"] && T.ownerDocument && T.ownerDocument.doctype && T.ownerDocument.doctype.name && re(Yo, T.ownerDocument.doctype.name) && (_e = "<!DOCTYPE " + T.ownerDocument.doctype.name + `>
` + _e), at && En([H, ce, J], (Be) => {
      _e = Zt(_e, Be, " ");
    }), b && Et ? b.createHTML(_e) : _e;
  }, e.setConfig = function() {
    let R = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    Xn(R), qt = !0;
  }, e.clearConfig = function() {
    St = null, qt = !1;
  }, e.isValidAttribute = function(R, _, T) {
    St || Xn({});
    const C = Q(R), j = Q(_);
    return xl(C, j, T);
  }, e.addHook = function(R, _) {
    typeof _ == "function" && (F[R] = F[R] || [], Xt(F[R], _));
  }, e.removeHook = function(R) {
    if (F[R])
      return qi(F[R]);
  }, e.removeHooks = function(R) {
    F[R] && (F[R] = []);
  }, e.removeAllHooks = function() {
    F = {};
  }, e;
}
Xo();
const {
  SvelteComponent: dc,
  append: Zo,
  attr: V,
  bubble: mc,
  check_outros: hc,
  create_slot: Ko,
  detach: nn,
  element: zn,
  empty: gc,
  get_all_dirty_from_scope: Jo,
  get_slot_changes: Qo,
  group_outros: bc,
  init: pc,
  insert: ln,
  listen: wc,
  safe_not_equal: kc,
  set_style: ge,
  space: xo,
  src_url_equal: Rn,
  toggle_class: Ot,
  transition_in: In,
  transition_out: Dn,
  update_slot_base: $o
} = window.__gradio__svelte__internal;
function vc(n) {
  let e, t, l, i, o, s, f = (
    /*icon*/
    n[7] && Yi(n)
  );
  const r = (
    /*#slots*/
    n[12].default
  ), a = Ko(
    r,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = zn("button"), f && f.c(), t = xo(), a && a.c(), V(e, "class", l = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), V(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), e.disabled = /*disabled*/
      n[8], Ot(e, "hidden", !/*visible*/
      n[2]), ge(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), ge(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), ge(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(c, u) {
      ln(c, e, u), f && f.m(e, null), Zo(e, t), a && a.m(e, null), i = !0, o || (s = wc(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), o = !0);
    },
    p(c, u) {
      /*icon*/
      c[7] ? f ? f.p(c, u) : (f = Yi(c), f.c(), f.m(e, t)) : f && (f.d(1), f = null), a && a.p && (!i || u & /*$$scope*/
      2048) && $o(
        a,
        r,
        c,
        /*$$scope*/
        c[11],
        i ? Qo(
          r,
          /*$$scope*/
          c[11],
          u,
          null
        ) : Jo(
          /*$$scope*/
          c[11]
        ),
        null
      ), (!i || u & /*size, variant, elem_classes*/
      26 && l !== (l = /*size*/
      c[4] + " " + /*variant*/
      c[3] + " " + /*elem_classes*/
      c[1].join(" ") + " svelte-8huxfn")) && V(e, "class", l), (!i || u & /*elem_id*/
      1) && V(
        e,
        "id",
        /*elem_id*/
        c[0]
      ), (!i || u & /*disabled*/
      256) && (e.disabled = /*disabled*/
      c[8]), (!i || u & /*size, variant, elem_classes, visible*/
      30) && Ot(e, "hidden", !/*visible*/
      c[2]), u & /*scale*/
      512 && ge(
        e,
        "flex-grow",
        /*scale*/
        c[9]
      ), u & /*scale*/
      512 && ge(
        e,
        "width",
        /*scale*/
        c[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && ge(e, "min-width", typeof /*min_width*/
      c[10] == "number" ? `calc(min(${/*min_width*/
      c[10]}px, 100%))` : null);
    },
    i(c) {
      i || (In(a, c), i = !0);
    },
    o(c) {
      Dn(a, c), i = !1;
    },
    d(c) {
      c && nn(e), f && f.d(), a && a.d(c), o = !1, s();
    }
  };
}
function Ec(n) {
  let e, t, l, i, o = (
    /*icon*/
    n[7] && Xi(n)
  );
  const s = (
    /*#slots*/
    n[12].default
  ), f = Ko(
    s,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = zn("a"), o && o.c(), t = xo(), f && f.c(), V(
        e,
        "href",
        /*link*/
        n[6]
      ), V(e, "rel", "noopener noreferrer"), V(
        e,
        "aria-disabled",
        /*disabled*/
        n[8]
      ), V(e, "class", l = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), V(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), Ot(e, "hidden", !/*visible*/
      n[2]), Ot(
        e,
        "disabled",
        /*disabled*/
        n[8]
      ), ge(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), ge(
        e,
        "pointer-events",
        /*disabled*/
        n[8] ? "none" : null
      ), ge(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), ge(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(r, a) {
      ln(r, e, a), o && o.m(e, null), Zo(e, t), f && f.m(e, null), i = !0;
    },
    p(r, a) {
      /*icon*/
      r[7] ? o ? o.p(r, a) : (o = Xi(r), o.c(), o.m(e, t)) : o && (o.d(1), o = null), f && f.p && (!i || a & /*$$scope*/
      2048) && $o(
        f,
        s,
        r,
        /*$$scope*/
        r[11],
        i ? Qo(
          s,
          /*$$scope*/
          r[11],
          a,
          null
        ) : Jo(
          /*$$scope*/
          r[11]
        ),
        null
      ), (!i || a & /*link*/
      64) && V(
        e,
        "href",
        /*link*/
        r[6]
      ), (!i || a & /*disabled*/
      256) && V(
        e,
        "aria-disabled",
        /*disabled*/
        r[8]
      ), (!i || a & /*size, variant, elem_classes*/
      26 && l !== (l = /*size*/
      r[4] + " " + /*variant*/
      r[3] + " " + /*elem_classes*/
      r[1].join(" ") + " svelte-8huxfn")) && V(e, "class", l), (!i || a & /*elem_id*/
      1) && V(
        e,
        "id",
        /*elem_id*/
        r[0]
      ), (!i || a & /*size, variant, elem_classes, visible*/
      30) && Ot(e, "hidden", !/*visible*/
      r[2]), (!i || a & /*size, variant, elem_classes, disabled*/
      282) && Ot(
        e,
        "disabled",
        /*disabled*/
        r[8]
      ), a & /*scale*/
      512 && ge(
        e,
        "flex-grow",
        /*scale*/
        r[9]
      ), a & /*disabled*/
      256 && ge(
        e,
        "pointer-events",
        /*disabled*/
        r[8] ? "none" : null
      ), a & /*scale*/
      512 && ge(
        e,
        "width",
        /*scale*/
        r[9] === 0 ? "fit-content" : null
      ), a & /*min_width*/
      1024 && ge(e, "min-width", typeof /*min_width*/
      r[10] == "number" ? `calc(min(${/*min_width*/
      r[10]}px, 100%))` : null);
    },
    i(r) {
      i || (In(f, r), i = !0);
    },
    o(r) {
      Dn(f, r), i = !1;
    },
    d(r) {
      r && nn(e), o && o.d(), f && f.d(r);
    }
  };
}
function Yi(n) {
  let e, t, l;
  return {
    c() {
      e = zn("img"), V(e, "class", "button-icon svelte-8huxfn"), Rn(e.src, t = /*icon*/
      n[7].url) || V(e, "src", t), V(e, "alt", l = `${/*value*/
      n[5]} icon`);
    },
    m(i, o) {
      ln(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !Rn(e.src, t = /*icon*/
      i[7].url) && V(e, "src", t), o & /*value*/
      32 && l !== (l = `${/*value*/
      i[5]} icon`) && V(e, "alt", l);
    },
    d(i) {
      i && nn(e);
    }
  };
}
function Xi(n) {
  let e, t, l;
  return {
    c() {
      e = zn("img"), V(e, "class", "button-icon svelte-8huxfn"), Rn(e.src, t = /*icon*/
      n[7].url) || V(e, "src", t), V(e, "alt", l = `${/*value*/
      n[5]} icon`);
    },
    m(i, o) {
      ln(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !Rn(e.src, t = /*icon*/
      i[7].url) && V(e, "src", t), o & /*value*/
      32 && l !== (l = `${/*value*/
      i[5]} icon`) && V(e, "alt", l);
    },
    d(i) {
      i && nn(e);
    }
  };
}
function Tc(n) {
  let e, t, l, i;
  const o = [Ec, vc], s = [];
  function f(r, a) {
    return (
      /*link*/
      r[6] && /*link*/
      r[6].length > 0 ? 0 : 1
    );
  }
  return e = f(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = gc();
    },
    m(r, a) {
      s[e].m(r, a), ln(r, l, a), i = !0;
    },
    p(r, [a]) {
      let c = e;
      e = f(r), e === c ? s[e].p(r, a) : (bc(), Dn(s[c], 1, 1, () => {
        s[c] = null;
      }), hc(), t = s[e], t ? t.p(r, a) : (t = s[e] = o[e](r), t.c()), In(t, 1), t.m(l.parentNode, l));
    },
    i(r) {
      i || (In(t), i = !0);
    },
    o(r) {
      Dn(t), i = !1;
    },
    d(r) {
      r && nn(l), s[e].d(r);
    }
  };
}
function yc(n, e, t) {
  let {
    $$slots: l = {},
    $$scope: i
  } = e, {
    elem_id: o = ""
  } = e, {
    elem_classes: s = []
  } = e, {
    visible: f = !0
  } = e, {
    variant: r = "secondary"
  } = e, {
    size: a = "lg"
  } = e, {
    value: c = null
  } = e, {
    link: u = null
  } = e, {
    icon: d = null
  } = e, {
    disabled: h = !1
  } = e, {
    scale: p = null
  } = e, {
    min_width: y = void 0
  } = e;
  function L(E) {
    mc.call(this, n, E);
  }
  return n.$$set = (E) => {
    "elem_id" in E && t(0, o = E.elem_id), "elem_classes" in E && t(1, s = E.elem_classes), "visible" in E && t(2, f = E.visible), "variant" in E && t(3, r = E.variant), "size" in E && t(4, a = E.size), "value" in E && t(5, c = E.value), "link" in E && t(6, u = E.link), "icon" in E && t(7, d = E.icon), "disabled" in E && t(8, h = E.disabled), "scale" in E && t(9, p = E.scale), "min_width" in E && t(10, y = E.min_width), "$$scope" in E && t(11, i = E.$$scope);
  }, [o, s, f, r, a, c, u, d, h, p, y, i, l, L];
}
class Ac extends dc {
  constructor(e) {
    super(), pc(this, e, yc, Tc, kc, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
var Sc = Object.defineProperty, Cc = (n, e, t) => e in n ? Sc(n, e, {
  enumerable: !0,
  configurable: !0,
  writable: !0,
  value: t
}) : n[e] = t, xe = (n, e, t) => (Cc(n, typeof e != "symbol" ? e + "" : e, t), t), ea = (n, e, t) => {
  if (!e.has(n)) throw TypeError("Cannot " + t);
}, xt = (n, e, t) => (ea(n, e, "read from private field"), t ? t.call(n) : e.get(n)), Lc = (n, e, t) => {
  if (e.has(n)) throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(n) : e.set(n, t);
}, Rc = (n, e, t, l) => (ea(n, e, "write to private field"), e.set(n, t), t), ct;
new Intl.Collator(0, {
  numeric: 1
}).compare;
class ml {
  constructor({
    path: e,
    url: t,
    orig_name: l,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: f,
    alt_text: r
  }) {
    xe(this, "path"), xe(this, "url"), xe(this, "orig_name"), xe(this, "size"), xe(this, "blob"), xe(this, "is_stream"), xe(this, "mime_type"), xe(this, "alt_text"), xe(this, "meta", {
      _type: "gradio.FileData"
    }), this.path = e, this.url = t, this.orig_name = l, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = f, this.alt_text = r;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class C_ extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = {
    allowCR: !1
  }) {
    super({
      transform: (t, l) => {
        for (t = xt(this, ct) + t; ; ) {
          const i = t.indexOf(`
`), o = e.allowCR ? t.indexOf("\r") : -1;
          if (o !== -1 && o !== t.length - 1 && (i === -1 || i - 1 > o)) {
            l.enqueue(t.slice(0, o)), t = t.slice(o + 1);
            continue;
          }
          if (i === -1) break;
          const s = t[i - 1] === "\r" ? i - 1 : i;
          l.enqueue(t.slice(0, s)), t = t.slice(i + 1);
        }
        Rc(this, ct, t);
      },
      flush: (t) => {
        if (xt(this, ct) === "") return;
        const l = e.allowCR && xt(this, ct).endsWith("\r") ? xt(this, ct).slice(0, -1) : xt(this, ct);
        t.enqueue(l);
      }
    }), Lc(this, ct, "");
  }
}
ct = /* @__PURE__ */ new WeakMap();
const {
  setContext: L_,
  getContext: Ic
} = window.__gradio__svelte__internal, Dc = "WORKER_PROXY_CONTEXT_KEY";
function Oc() {
  return Ic(Dc);
}
function Nc(n) {
  return n.host === window.location.host || n.host === "localhost:7860" || n.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  n.host === "lite.local";
}
function Mc(n, e) {
  const t = e.toLowerCase();
  for (const [l, i] of Object.entries(n))
    if (l.toLowerCase() === t)
      return i;
}
function Pc(n) {
  if (n == null)
    return !1;
  const e = new URL(n, window.location.href);
  return !(!Nc(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: Fc,
  assign: On,
  check_outros: ta,
  compute_rest_props: Zi,
  create_slot: Pl,
  detach: qn,
  element: na,
  empty: la,
  exclude_internal_props: Uc,
  get_all_dirty_from_scope: Fl,
  get_slot_changes: Ul,
  get_spread_update: ia,
  group_outros: oa,
  init: zc,
  insert: Hn,
  listen: aa,
  prevent_default: qc,
  safe_not_equal: Hc,
  set_attributes: Nn,
  transition_in: wt,
  transition_out: kt,
  update_slot_base: zl
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Bc
} = window.__gradio__svelte__internal;
function jc(n) {
  let e, t, l, i, o;
  const s = (
    /*#slots*/
    n[8].default
  ), f = Pl(
    s,
    n,
    /*$$scope*/
    n[7],
    null
  );
  let r = [
    {
      href: (
        /*href*/
        n[0]
      )
    },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    {
      rel: "noopener noreferrer"
    },
    {
      download: (
        /*download*/
        n[1]
      )
    },
    /*$$restProps*/
    n[6]
  ], a = {};
  for (let c = 0; c < r.length; c += 1)
    a = On(a, r[c]);
  return {
    c() {
      e = na("a"), f && f.c(), Nn(e, a);
    },
    m(c, u) {
      Hn(c, e, u), f && f.m(e, null), l = !0, i || (o = aa(
        e,
        "click",
        /*dispatch*/
        n[3].bind(null, "click")
      ), i = !0);
    },
    p(c, u) {
      f && f.p && (!l || u & /*$$scope*/
      128) && zl(
        f,
        s,
        c,
        /*$$scope*/
        c[7],
        l ? Ul(
          s,
          /*$$scope*/
          c[7],
          u,
          null
        ) : Fl(
          /*$$scope*/
          c[7]
        ),
        null
      ), Nn(e, a = ia(r, [(!l || u & /*href*/
      1) && {
        href: (
          /*href*/
          c[0]
        )
      }, {
        target: t
      }, {
        rel: "noopener noreferrer"
      }, (!l || u & /*download*/
      2) && {
        download: (
          /*download*/
          c[1]
        )
      }, u & /*$$restProps*/
      64 && /*$$restProps*/
      c[6]]));
    },
    i(c) {
      l || (wt(f, c), l = !0);
    },
    o(c) {
      kt(f, c), l = !1;
    },
    d(c) {
      c && qn(e), f && f.d(c), i = !1, o();
    }
  };
}
function Wc(n) {
  let e, t, l, i;
  const o = [Vc, Gc], s = [];
  function f(r, a) {
    return (
      /*is_downloading*/
      r[2] ? 0 : 1
    );
  }
  return e = f(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = la();
    },
    m(r, a) {
      s[e].m(r, a), Hn(r, l, a), i = !0;
    },
    p(r, a) {
      let c = e;
      e = f(r), e === c ? s[e].p(r, a) : (oa(), kt(s[c], 1, 1, () => {
        s[c] = null;
      }), ta(), t = s[e], t ? t.p(r, a) : (t = s[e] = o[e](r), t.c()), wt(t, 1), t.m(l.parentNode, l));
    },
    i(r) {
      i || (wt(t), i = !0);
    },
    o(r) {
      kt(t), i = !1;
    },
    d(r) {
      r && qn(l), s[e].d(r);
    }
  };
}
function Gc(n) {
  let e, t, l, i;
  const o = (
    /*#slots*/
    n[8].default
  ), s = Pl(
    o,
    n,
    /*$$scope*/
    n[7],
    null
  );
  let f = [
    /*$$restProps*/
    n[6],
    {
      href: (
        /*href*/
        n[0]
      )
    }
  ], r = {};
  for (let a = 0; a < f.length; a += 1)
    r = On(r, f[a]);
  return {
    c() {
      e = na("a"), s && s.c(), Nn(e, r);
    },
    m(a, c) {
      Hn(a, e, c), s && s.m(e, null), t = !0, l || (i = aa(e, "click", qc(
        /*wasm_click_handler*/
        n[5]
      )), l = !0);
    },
    p(a, c) {
      s && s.p && (!t || c & /*$$scope*/
      128) && zl(
        s,
        o,
        a,
        /*$$scope*/
        a[7],
        t ? Ul(
          o,
          /*$$scope*/
          a[7],
          c,
          null
        ) : Fl(
          /*$$scope*/
          a[7]
        ),
        null
      ), Nn(e, r = ia(f, [c & /*$$restProps*/
      64 && /*$$restProps*/
      a[6], (!t || c & /*href*/
      1) && {
        href: (
          /*href*/
          a[0]
        )
      }]));
    },
    i(a) {
      t || (wt(s, a), t = !0);
    },
    o(a) {
      kt(s, a), t = !1;
    },
    d(a) {
      a && qn(e), s && s.d(a), l = !1, i();
    }
  };
}
function Vc(n) {
  let e;
  const t = (
    /*#slots*/
    n[8].default
  ), l = Pl(
    t,
    n,
    /*$$scope*/
    n[7],
    null
  );
  return {
    c() {
      l && l.c();
    },
    m(i, o) {
      l && l.m(i, o), e = !0;
    },
    p(i, o) {
      l && l.p && (!e || o & /*$$scope*/
      128) && zl(
        l,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? Ul(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : Fl(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (wt(l, i), e = !0);
    },
    o(i) {
      kt(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function Yc(n) {
  let e, t, l, i, o;
  const s = [Wc, jc], f = [];
  function r(a, c) {
    return c & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (a[4] && Pc(
      /*href*/
      a[0]
    ))), e ? 0 : 1;
  }
  return t = r(n, -1), l = f[t] = s[t](n), {
    c() {
      l.c(), i = la();
    },
    m(a, c) {
      f[t].m(a, c), Hn(a, i, c), o = !0;
    },
    p(a, [c]) {
      let u = t;
      t = r(a, c), t === u ? f[t].p(a, c) : (oa(), kt(f[u], 1, 1, () => {
        f[u] = null;
      }), ta(), l = f[t], l ? l.p(a, c) : (l = f[t] = s[t](a), l.c()), wt(l, 1), l.m(i.parentNode, i));
    },
    i(a) {
      o || (wt(l), o = !0);
    },
    o(a) {
      kt(l), o = !1;
    },
    d(a) {
      a && qn(i), f[t].d(a);
    }
  };
}
function Xc(n, e, t) {
  const l = ["href", "download"];
  let i = Zi(e, l), {
    $$slots: o = {},
    $$scope: s
  } = e;
  var f = this && this.__awaiter || function(p, y, L, E) {
    function g(v) {
      return v instanceof L ? v : new L(function(b) {
        b(v);
      });
    }
    return new (L || (L = Promise))(function(v, b) {
      function S(A) {
        try {
          I(E.next(A));
        } catch (Z) {
          b(Z);
        }
      }
      function w(A) {
        try {
          I(E.throw(A));
        } catch (Z) {
          b(Z);
        }
      }
      function I(A) {
        A.done ? v(A.value) : g(A.value).then(S, w);
      }
      I((E = E.apply(p, y || [])).next());
    });
  };
  let {
    href: r = void 0
  } = e, {
    download: a
  } = e;
  const c = Bc();
  let u = !1;
  const d = Oc();
  function h() {
    return f(this, void 0, void 0, function* () {
      if (u)
        return;
      if (c("click"), r == null)
        throw new Error("href is not defined.");
      if (d == null)
        throw new Error("Wasm worker proxy is not available.");
      const y = new URL(r, window.location.href).pathname;
      t(2, u = !0), d.httpRequest({
        method: "GET",
        path: y,
        headers: {},
        query_string: ""
      }).then((L) => {
        if (L.status !== 200)
          throw new Error(`Failed to get file ${y} from the Wasm worker.`);
        const E = new Blob([L.body], {
          type: Mc(L.headers, "content-type")
        }), g = URL.createObjectURL(E), v = document.createElement("a");
        v.href = g, v.download = a, v.click(), URL.revokeObjectURL(g);
      }).finally(() => {
        t(2, u = !1);
      });
    });
  }
  return n.$$set = (p) => {
    e = On(On({}, e), Uc(p)), t(6, i = Zi(e, l)), "href" in p && t(0, r = p.href), "download" in p && t(1, a = p.download), "$$scope" in p && t(7, s = p.$$scope);
  }, [r, a, u, c, d, h, i, s, o];
}
class Zc extends Fc {
  constructor(e) {
    super(), zc(this, e, Xc, Yc, Hc, {
      href: 0,
      download: 1
    });
  }
}
const {
  SvelteComponent: Kc,
  append: hl,
  attr: Jc,
  check_outros: gl,
  create_component: on,
  destroy_component: an,
  detach: Qc,
  element: xc,
  group_outros: bl,
  init: $c,
  insert: eu,
  mount_component: rn,
  safe_not_equal: tu,
  set_style: Ki,
  space: pl,
  toggle_class: Ji,
  transition_in: he,
  transition_out: Me
} = window.__gradio__svelte__internal, {
  createEventDispatcher: nu
} = window.__gradio__svelte__internal;
function Qi(n) {
  let e, t;
  return e = new dt({
    props: {
      Icon: ss,
      label: (
        /*i18n*/
        n[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[6]
  ), {
    c() {
      on(e.$$.fragment);
    },
    m(l, i) {
      rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.edit")), e.$set(o);
    },
    i(l) {
      t || (he(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Me(e.$$.fragment, l), t = !1;
    },
    d(l) {
      an(e, l);
    }
  };
}
function xi(n) {
  let e, t;
  return e = new dt({
    props: {
      Icon: Rs,
      label: (
        /*i18n*/
        n[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    n[7]
  ), {
    c() {
      on(e.$$.fragment);
    },
    m(l, i) {
      rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.undo")), e.$set(o);
    },
    i(l) {
      t || (he(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Me(e.$$.fragment, l), t = !1;
    },
    d(l) {
      an(e, l);
    }
  };
}
function $i(n) {
  let e, t;
  return e = new Zc({
    props: {
      href: (
        /*download*/
        n[2]
      ),
      download: !0,
      $$slots: {
        default: [lu]
      },
      $$scope: {
        ctx: n
      }
    }
  }), {
    c() {
      on(e.$$.fragment);
    },
    m(l, i) {
      rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      l[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = {
        dirty: i,
        ctx: l
      }), e.$set(o);
    },
    i(l) {
      t || (he(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Me(e.$$.fragment, l), t = !1;
    },
    d(l) {
      an(e, l);
    }
  };
}
function lu(n) {
  let e, t;
  return e = new dt({
    props: {
      Icon: Co,
      label: (
        /*i18n*/
        n[4]("common.download")
      )
    }
  }), {
    c() {
      on(e.$$.fragment);
    },
    m(l, i) {
      rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.download")), e.$set(o);
    },
    i(l) {
      t || (he(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Me(e.$$.fragment, l), t = !1;
    },
    d(l) {
      an(e, l);
    }
  };
}
function iu(n) {
  let e, t, l, i, o, s, f = (
    /*editable*/
    n[0] && Qi(n)
  ), r = (
    /*undoable*/
    n[1] && xi(n)
  ), a = (
    /*download*/
    n[2] && $i(n)
  );
  return o = new dt({
    props: {
      Icon: qr,
      label: (
        /*i18n*/
        n[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    n[8]
  ), {
    c() {
      e = xc("div"), f && f.c(), t = pl(), r && r.c(), l = pl(), a && a.c(), i = pl(), on(o.$$.fragment), Jc(e, "class", "svelte-1wj0ocy"), Ji(e, "not-absolute", !/*absolute*/
      n[3]), Ki(
        e,
        "position",
        /*absolute*/
        n[3] ? "absolute" : "static"
      );
    },
    m(c, u) {
      eu(c, e, u), f && f.m(e, null), hl(e, t), r && r.m(e, null), hl(e, l), a && a.m(e, null), hl(e, i), rn(o, e, null), s = !0;
    },
    p(c, [u]) {
      /*editable*/
      c[0] ? f ? (f.p(c, u), u & /*editable*/
      1 && he(f, 1)) : (f = Qi(c), f.c(), he(f, 1), f.m(e, t)) : f && (bl(), Me(f, 1, 1, () => {
        f = null;
      }), gl()), /*undoable*/
      c[1] ? r ? (r.p(c, u), u & /*undoable*/
      2 && he(r, 1)) : (r = xi(c), r.c(), he(r, 1), r.m(e, l)) : r && (bl(), Me(r, 1, 1, () => {
        r = null;
      }), gl()), /*download*/
      c[2] ? a ? (a.p(c, u), u & /*download*/
      4 && he(a, 1)) : (a = $i(c), a.c(), he(a, 1), a.m(e, i)) : a && (bl(), Me(a, 1, 1, () => {
        a = null;
      }), gl());
      const d = {};
      u & /*i18n*/
      16 && (d.label = /*i18n*/
      c[4]("common.clear")), o.$set(d), (!s || u & /*absolute*/
      8) && Ji(e, "not-absolute", !/*absolute*/
      c[3]), u & /*absolute*/
      8 && Ki(
        e,
        "position",
        /*absolute*/
        c[3] ? "absolute" : "static"
      );
    },
    i(c) {
      s || (he(f), he(r), he(a), he(o.$$.fragment, c), s = !0);
    },
    o(c) {
      Me(f), Me(r), Me(a), Me(o.$$.fragment, c), s = !1;
    },
    d(c) {
      c && Qc(e), f && f.d(), r && r.d(), a && a.d(), an(o);
    }
  };
}
function ou(n, e, t) {
  let {
    editable: l = !1
  } = e, {
    undoable: i = !1
  } = e, {
    download: o = null
  } = e, {
    absolute: s = !0
  } = e, {
    i18n: f
  } = e;
  const r = nu(), a = () => r("edit"), c = () => r("undo"), u = (d) => {
    r("clear"), d.stopPropagation();
  };
  return n.$$set = (d) => {
    "editable" in d && t(0, l = d.editable), "undoable" in d && t(1, i = d.undoable), "download" in d && t(2, o = d.download), "absolute" in d && t(3, s = d.absolute), "i18n" in d && t(4, f = d.i18n);
  }, [l, i, o, s, f, r, a, c, u];
}
class au extends Kc {
  constructor(e) {
    super(), $c(this, e, ou, iu, tu, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
function ra(n, e, t) {
  if (n == null)
    return null;
  if (Array.isArray(n)) {
    const l = [];
    for (const i of n)
      i == null ? l.push(null) : l.push(ra(i, e, t));
    return l;
  }
  return n.is_stream ? t == null ? new ml({
    ...n,
    url: e + "/stream/" + n.path
  }) : new ml({
    ...n,
    url: "/proxy=" + t + "stream/" + n.path
  }) : new ml({
    ...n,
    url: su(n.path, e, t)
  });
}
function ru(n) {
  try {
    const e = new URL(n);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function su(n, e, t) {
  return n == null ? t ? `/proxy=${t}file=` : `${e}/file=` : ru(n) ? n : t ? `/proxy=${t}file=${n}` : `${e}/file=${n}`;
}
var eo = Object.prototype.hasOwnProperty;
function to(n, e, t) {
  for (t of n.keys())
    if ($t(t, e)) return t;
}
function $t(n, e) {
  var t, l, i;
  if (n === e) return !0;
  if (n && e && (t = n.constructor) === e.constructor) {
    if (t === Date) return n.getTime() === e.getTime();
    if (t === RegExp) return n.toString() === e.toString();
    if (t === Array) {
      if ((l = n.length) === e.length)
        for (; l-- && $t(n[l], e[l]); ) ;
      return l === -1;
    }
    if (t === Set) {
      if (n.size !== e.size)
        return !1;
      for (l of n)
        if (i = l, i && typeof i == "object" && (i = to(e, i), !i) || !e.has(i)) return !1;
      return !0;
    }
    if (t === Map) {
      if (n.size !== e.size)
        return !1;
      for (l of n)
        if (i = l[0], i && typeof i == "object" && (i = to(e, i), !i) || !$t(l[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      n = new Uint8Array(n), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((l = n.byteLength) === e.byteLength)
        for (; l-- && n.getInt8(l) === e.getInt8(l); ) ;
      return l === -1;
    }
    if (ArrayBuffer.isView(n)) {
      if ((l = n.byteLength) === e.byteLength)
        for (; l-- && n[l] === e[l]; ) ;
      return l === -1;
    }
    if (!t || typeof n == "object") {
      l = 0;
      for (t in n)
        if (eo.call(n, t) && ++l && !eo.call(e, t) || !(t in e) || !$t(n[t], e[t])) return !1;
      return Object.keys(e).length === l;
    }
  }
  return n !== n && e !== e;
}
const {
  SvelteComponent: fu,
  append: no,
  attr: le,
  detach: cu,
  init: uu,
  insert: _u,
  noop: lo,
  safe_not_equal: du,
  svg_element: wl
} = window.__gradio__svelte__internal;
function mu(n) {
  let e, t, l, i;
  return {
    c() {
      e = wl("svg"), t = wl("path"), l = wl("path"), le(t, "stroke", "currentColor"), le(t, "stroke-width", "1.5"), le(t, "stroke-linecap", "round"), le(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), le(l, "stroke", "currentColor"), le(l, "stroke-width", "1.5"), le(l, "stroke-linecap", "round"), le(l, "stroke-linejoin", "round"), le(l, "d", "M7 20V9"), le(e, "xmlns", "http://www.w3.org/2000/svg"), le(e, "viewBox", "0 0 24 24"), le(e, "fill", i = /*selected*/
      n[0] ? "currentColor" : "none"), le(e, "stroke-width", "1.5"), le(e, "color", "currentColor"), le(e, "transform", "rotate(180)");
    },
    m(o, s) {
      _u(o, e, s), no(e, t), no(e, l);
    },
    p(o, [s]) {
      s & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && le(e, "fill", i);
    },
    i: lo,
    o: lo,
    d(o) {
      o && cu(e);
    }
  };
}
function hu(n, e, t) {
  let {
    selected: l
  } = e;
  return n.$$set = (i) => {
    "selected" in i && t(0, l = i.selected);
  }, [l];
}
class gu extends fu {
  constructor(e) {
    super(), uu(this, e, hu, mu, du, {
      selected: 0
    });
  }
}
const {
  SvelteComponent: bu,
  append: tt,
  attr: Ve,
  check_outros: pu,
  create_component: io,
  destroy_component: oo,
  detach: Bn,
  element: pt,
  flush: yn,
  group_outros: wu,
  init: ku,
  insert: jn,
  listen: sa,
  mount_component: ao,
  safe_not_equal: vu,
  set_data: fa,
  set_style: Eu,
  space: Cn,
  src_url_equal: ro,
  text: ca,
  transition_in: en,
  transition_out: Mn
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Tu
} = window.__gradio__svelte__internal;
function so(n) {
  let e, t = (
    /*value*/
    n[0].caption + ""
  ), l;
  return {
    c() {
      e = pt("div"), l = ca(t), Ve(e, "class", "foot-label left-label svelte-u350v8");
    },
    m(i, o) {
      jn(i, e, o), tt(e, l);
    },
    p(i, o) {
      o & /*value*/
      1 && t !== (t = /*value*/
      i[0].caption + "") && fa(l, t);
    },
    d(i) {
      i && Bn(e);
    }
  };
}
function fo(n) {
  let e, t, l, i;
  return {
    c() {
      e = pt("button"), t = ca(
        /*action_label*/
        n[3]
      ), Ve(e, "class", "foot-label right-label svelte-u350v8");
    },
    m(o, s) {
      jn(o, e, s), tt(e, t), l || (i = sa(
        e,
        "click",
        /*click_handler_1*/
        n[6]
      ), l = !0);
    },
    p(o, s) {
      s & /*action_label*/
      8 && fa(
        t,
        /*action_label*/
        o[3]
      );
    },
    d(o) {
      o && Bn(e), l = !1, i();
    }
  };
}
function co(n) {
  let e, t, l, i, o, s, f;
  return l = new dt({
    props: {
      size: "large",
      highlight: (
        /*value*/
        n[0].liked
      ),
      Icon: Es
    }
  }), l.$on(
    "click",
    /*click_handler_2*/
    n[7]
  ), s = new dt({
    props: {
      size: "large",
      highlight: (
        /*value*/
        n[0].liked === !1
      ),
      Icon: gu
    }
  }), s.$on(
    "click",
    /*click_handler_3*/
    n[8]
  ), {
    c() {
      e = pt("div"), t = pt("span"), io(l.$$.fragment), i = Cn(), o = pt("span"), io(s.$$.fragment), Eu(t, "margin-right", "1px"), Ve(e, "class", "like-button svelte-u350v8");
    },
    m(r, a) {
      jn(r, e, a), tt(e, t), ao(l, t, null), tt(e, i), tt(e, o), ao(s, o, null), f = !0;
    },
    p(r, a) {
      const c = {};
      a & /*value*/
      1 && (c.highlight = /*value*/
      r[0].liked), l.$set(c);
      const u = {};
      a & /*value*/
      1 && (u.highlight = /*value*/
      r[0].liked === !1), s.$set(u);
    },
    i(r) {
      f || (en(l.$$.fragment, r), en(s.$$.fragment, r), f = !0);
    },
    o(r) {
      Mn(l.$$.fragment, r), Mn(s.$$.fragment, r), f = !1;
    },
    d(r) {
      r && Bn(e), oo(l), oo(s);
    }
  };
}
function yu(n) {
  let e, t, l, i, o, s, f, r, a, c, u = (
    /*value*/
    n[0].caption && so(n)
  ), d = (
    /*clickable*/
    n[2] && fo(n)
  ), h = (
    /*likeable*/
    n[1] && co(n)
  );
  return {
    c() {
      e = pt("div"), t = pt("img"), o = Cn(), u && u.c(), s = Cn(), d && d.c(), f = Cn(), h && h.c(), Ve(t, "alt", l = /*value*/
      n[0].caption || ""), ro(t.src, i = /*value*/
      n[0].image.url) || Ve(t, "src", i), Ve(t, "class", "thumbnail-img svelte-u350v8"), Ve(t, "loading", "lazy"), Ve(e, "class", "thumbnail-image-box svelte-u350v8");
    },
    m(p, y) {
      jn(p, e, y), tt(e, t), tt(e, o), u && u.m(e, null), tt(e, s), d && d.m(e, null), tt(e, f), h && h.m(e, null), r = !0, a || (c = sa(
        t,
        "click",
        /*click_handler*/
        n[5]
      ), a = !0);
    },
    p(p, [y]) {
      (!r || y & /*value*/
      1 && l !== (l = /*value*/
      p[0].caption || "")) && Ve(t, "alt", l), (!r || y & /*value*/
      1 && !ro(t.src, i = /*value*/
      p[0].image.url)) && Ve(t, "src", i), /*value*/
      p[0].caption ? u ? u.p(p, y) : (u = so(p), u.c(), u.m(e, s)) : u && (u.d(1), u = null), /*clickable*/
      p[2] ? d ? d.p(p, y) : (d = fo(p), d.c(), d.m(e, f)) : d && (d.d(1), d = null), /*likeable*/
      p[1] ? h ? (h.p(p, y), y & /*likeable*/
      2 && en(h, 1)) : (h = co(p), h.c(), en(h, 1), h.m(e, null)) : h && (wu(), Mn(h, 1, 1, () => {
        h = null;
      }), pu());
    },
    i(p) {
      r || (en(h), r = !0);
    },
    o(p) {
      Mn(h), r = !1;
    },
    d(p) {
      p && Bn(e), u && u.d(), d && d.d(), h && h.d(), a = !1, c();
    }
  };
}
function Au(n, e, t) {
  const l = Tu();
  let {
    likeable: i
  } = e, {
    clickable: o
  } = e, {
    value: s
  } = e, {
    action_label: f
  } = e;
  const r = () => l("click"), a = () => {
    l("label_click");
  }, c = () => {
    if (s.liked) {
      t(0, s.liked = void 0, s), l("like", void 0);
      return;
    }
    t(0, s.liked = !0, s), l("like", !0);
  }, u = () => {
    if (s.liked === !1) {
      t(0, s.liked = void 0, s), l("like", void 0);
      return;
    }
    t(0, s.liked = !1, s), l("like", !1);
  };
  return n.$$set = (d) => {
    "likeable" in d && t(1, i = d.likeable), "clickable" in d && t(2, o = d.clickable), "value" in d && t(0, s = d.value), "action_label" in d && t(3, f = d.action_label);
  }, [s, i, o, f, l, r, a, c, u];
}
class Su extends bu {
  constructor(e) {
    super(), ku(this, e, Au, yu, vu, {
      likeable: 1,
      clickable: 2,
      value: 0,
      action_label: 3
    });
  }
  get likeable() {
    return this.$$.ctx[1];
  }
  set likeable(e) {
    this.$$set({
      likeable: e
    }), yn();
  }
  get clickable() {
    return this.$$.ctx[2];
  }
  set clickable(e) {
    this.$$set({
      clickable: e
    }), yn();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), yn();
  }
  get action_label() {
    return this.$$.ctx[3];
  }
  set action_label(e) {
    this.$$set({
      action_label: e
    }), yn();
  }
}
const kl = [{
  key: "xs",
  width: 0
}, {
  key: "sm",
  width: 576
}, {
  key: "md",
  width: 768
}, {
  key: "lg",
  width: 992
}, {
  key: "xl",
  width: 1200
}, {
  key: "xxl",
  width: 1600
}];
async function Cu(n) {
  if ("clipboard" in navigator)
    await navigator.clipboard.writeText(n);
  else {
    const e = document.createElement("textarea");
    e.value = n, e.style.position = "absolute", e.style.left = "-999999px", document.body.prepend(e), e.select();
    try {
      document.execCommand("copy");
    } catch (t) {
      return Promise.reject(t);
    } finally {
      e.remove();
    }
  }
}
async function Lu(n) {
  return n ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(n.map((t) => !t.image || !t.image.url ? "" : t.image.url))).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
function Ru(n) {
  let e = 0;
  for (let t = 0; t < n.length; t++) e = n[e] <= n[t] ? e : t;
  return e;
}
function Iu(n, {
  getWidth: e,
  setWidth: t,
  getHeight: l,
  setHeight: i,
  getPadding: o,
  setX: s,
  setY: f,
  getChildren: r
}, {
  cols: a,
  gap: c
}) {
  const [u, d, h, p] = o(n), y = r(n), L = y.length, [E, g] = Array.isArray(c) ? c : [c, c];
  if (L) {
    const v = (e(n) - E * (a - 1) - (p + d)) / a;
    y.forEach((w) => {
      t(w, v);
    });
    const b = y.map((w) => l(w)), S = Array(a).fill(u);
    for (let w = 0; w < L; w++) {
      const I = y[w], A = Ru(S);
      f(I, S[A]), s(I, p + (v + E) * A), S[A] += b[w] + g;
    }
    i(n, Math.max(...S) - g + h);
  } else
    i(n, u + h);
}
const uo = (n) => n.nodeType == 1, Ol = Symbol(), Nl = Symbol();
function Du(n, e) {
  let t, l, i = !1;
  function o() {
    i || (i = !0, requestAnimationFrame(() => {
      e(), n[Nl] = n.offsetWidth, n[Ol] = n.offsetHeight, i = !1;
    }));
  }
  function s() {
    n && (t = new ResizeObserver((r) => {
      r.some((a) => {
        const c = a.target;
        return c[Nl] !== c.offsetWidth || c[Ol] !== c.offsetHeight;
      }) && o();
    }), t.observe(n), Array.from(n.children).forEach((r) => {
      t.observe(r);
    }), l = new MutationObserver((r) => {
      r.forEach((a) => {
        a.addedNodes.forEach((c) => uo(c) && t.observe(c)), a.removedNodes.forEach((c) => uo(c) && t.unobserve(c));
      }), o();
    }), l.observe(n, {
      childList: !0,
      attributes: !1
    }), o());
  }
  function f() {
    t == null || t.disconnect(), l == null || l.disconnect();
  }
  return {
    layout: o,
    mount: s,
    unmount: f
  };
}
const Ou = (n, e) => Du(n, () => {
  Iu(n, {
    getWidth: (t) => t.offsetWidth,
    setWidth: (t, l) => t.style.width = l + "px",
    getHeight: (t) => (t[Nl] = t.offsetWidth, t[Ol] = t.offsetHeight),
    setHeight: (t, l) => t.style.height = l + "px",
    getPadding: (t) => {
      const l = getComputedStyle(t);
      return [parseInt(l.paddingTop), parseInt(l.paddingRight), parseInt(l.paddingBottom), parseInt(l.paddingLeft)];
    },
    setX: (t, l) => t.style.left = l + "px",
    setY: (t, l) => t.style.top = l + "px",
    getChildren: (t) => Array.from(t.children)
  }, e);
});
class Nu {
  constructor(e, t = {
    cols: 2,
    gap: 4
  }) {
    li(this, "_layout");
    this._layout = Ou(e, t), this._layout.mount();
  }
  unmount() {
    this._layout.unmount();
  }
  render() {
    this._layout.layout();
  }
}
const {
  SvelteComponent: Mu,
  add_iframe_resize_listener: Pu,
  add_render_callback: ua,
  append: te,
  assign: Fu,
  attr: M,
  binding_callbacks: vl,
  bubble: Uu,
  check_outros: gt,
  create_component: nt,
  destroy_component: lt,
  destroy_each: _a,
  detach: Ue,
  element: se,
  empty: zu,
  ensure_array_like: Pn,
  get_spread_object: qu,
  get_spread_update: Hu,
  globals: Bu,
  group_outros: bt,
  init: ju,
  insert: ze,
  listen: Fn,
  mount_component: it,
  noop: Wu,
  run_all: Gu,
  safe_not_equal: Vu,
  set_data: da,
  set_style: ut,
  space: Ze,
  src_url_equal: Un,
  text: ma,
  toggle_class: ye,
  transition_in: q,
  transition_out: Y
} = window.__gradio__svelte__internal, {
  window: Ml
} = Bu, {
  createEventDispatcher: Yu,
  onDestroy: Xu,
  tick: Zu
} = window.__gradio__svelte__internal;
function _o(n, e, t) {
  const l = n.slice();
  return l[57] = e[t], l[59] = t, l;
}
function mo(n, e, t) {
  const l = n.slice();
  return l[57] = e[t], l[60] = e, l[59] = t, l;
}
function ho(n) {
  let e, t;
  return e = new tr({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      Icon: Lo,
      label: (
        /*label*/
        n[4] || "Gallery"
      )
    }
  }), {
    c() {
      nt(e.$$.fragment);
    },
    m(l, i) {
      it(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      l[2]), i[0] & /*label*/
      16 && (o.label = /*label*/
      l[4] || "Gallery"), e.$set(o);
    },
    i(l) {
      t || (q(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Y(e.$$.fragment, l), t = !1;
    },
    d(l) {
      lt(e, l);
    }
  };
}
function Ku(n) {
  let e, t, l, i, o, s, f, r, a, c, u, d = (
    /*selected_image*/
    n[23] && /*allow_preview*/
    n[9] && go(n)
  ), h = (
    /*show_share_button*/
    n[10] && ko(n)
  ), p = Pn(
    /*resolved_value*/
    n[18]
  ), y = [];
  for (let b = 0; b < p.length; b += 1)
    y[b] = vo(_o(n, p, b));
  const L = (b) => Y(y[b], 1, 1, () => {
    y[b] = null;
  }), E = [xu, Qu], g = [];
  function v(b, S) {
    return (
      /*pending*/
      b[5] ? 0 : 1
    );
  }
  return r = v(n), a = g[r] = E[r](n), {
    c() {
      d && d.c(), e = Ze(), t = se("div"), l = se("div"), h && h.c(), i = Ze(), o = se("div");
      for (let b = 0; b < y.length; b += 1)
        y[b].c();
      s = Ze(), f = se("p"), a.c(), M(o, "class", "waterfall svelte-yk2d08"), M(l, "class", "grid-container svelte-yk2d08"), ut(
        l,
        "--object-fit",
        /*object_fit*/
        n[1]
      ), ut(
        l,
        "min-height",
        /*height*/
        n[8] + "px"
      ), ye(
        l,
        "pt-6",
        /*show_label*/
        n[2]
      ), M(f, "class", "loading-line svelte-yk2d08"), ye(f, "visible", !/*selected_image*/
      (n[23] && /*allow_preview*/
      n[9]) && /*has_more*/
      n[3]), M(t, "class", "grid-wrap svelte-yk2d08"), ut(
        t,
        "height",
        /*height*/
        n[8] + "px"
      ), ua(() => (
        /*div2_elementresize_handler*/
        n[51].call(t)
      )), ye(t, "fixed-height", !/*height*/
      n[8] || /*height*/
      n[8] === "auto");
    },
    m(b, S) {
      d && d.m(b, S), ze(b, e, S), ze(b, t, S), te(t, l), h && h.m(l, null), te(l, i), te(l, o);
      for (let w = 0; w < y.length; w += 1)
        y[w] && y[w].m(o, null);
      n[49](o), te(t, s), te(t, f), g[r].m(f, null), c = Pu(
        t,
        /*div2_elementresize_handler*/
        n[51].bind(t)
      ), u = !0;
    },
    p(b, S) {
      if (/*selected_image*/
      b[23] && /*allow_preview*/
      b[9] ? d ? (d.p(b, S), S[0] & /*selected_image, allow_preview*/
      8389120 && q(d, 1)) : (d = go(b), d.c(), q(d, 1), d.m(e.parentNode, e)) : d && (bt(), Y(d, 1, 1, () => {
        d = null;
      }), gt()), /*show_share_button*/
      b[10] ? h ? (h.p(b, S), S[0] & /*show_share_button*/
      1024 && q(h, 1)) : (h = ko(b), h.c(), q(h, 1), h.m(l, i)) : h && (bt(), Y(h, 1, 1, () => {
        h = null;
      }), gt()), S[0] & /*resolved_value, selected_index, likeable, clickable, action_label, dispatch*/
      17045569) {
        p = Pn(
          /*resolved_value*/
          b[18]
        );
        let I;
        for (I = 0; I < p.length; I += 1) {
          const A = _o(b, p, I);
          y[I] ? (y[I].p(A, S), q(y[I], 1)) : (y[I] = vo(A), y[I].c(), q(y[I], 1), y[I].m(o, null));
        }
        for (bt(), I = p.length; I < y.length; I += 1)
          L(I);
        gt();
      }
      (!u || S[0] & /*object_fit*/
      2) && ut(
        l,
        "--object-fit",
        /*object_fit*/
        b[1]
      ), (!u || S[0] & /*height*/
      256) && ut(
        l,
        "min-height",
        /*height*/
        b[8] + "px"
      ), (!u || S[0] & /*show_label*/
      4) && ye(
        l,
        "pt-6",
        /*show_label*/
        b[2]
      );
      let w = r;
      r = v(b), r === w ? g[r].p(b, S) : (bt(), Y(g[w], 1, 1, () => {
        g[w] = null;
      }), gt(), a = g[r], a ? a.p(b, S) : (a = g[r] = E[r](b), a.c()), q(a, 1), a.m(f, null)), (!u || S[0] & /*selected_image, allow_preview, has_more*/
      8389128) && ye(f, "visible", !/*selected_image*/
      (b[23] && /*allow_preview*/
      b[9]) && /*has_more*/
      b[3]), (!u || S[0] & /*height*/
      256) && ut(
        t,
        "height",
        /*height*/
        b[8] + "px"
      ), (!u || S[0] & /*height*/
      256) && ye(t, "fixed-height", !/*height*/
      b[8] || /*height*/
      b[8] === "auto");
    },
    i(b) {
      if (!u) {
        q(d), q(h);
        for (let S = 0; S < p.length; S += 1)
          q(y[S]);
        q(a), u = !0;
      }
    },
    o(b) {
      Y(d), Y(h), y = y.filter(Boolean);
      for (let S = 0; S < y.length; S += 1)
        Y(y[S]);
      Y(a), u = !1;
    },
    d(b) {
      b && (Ue(e), Ue(t)), d && d.d(b), h && h.d(), _a(y, b), n[49](null), g[r].d(), c();
    }
  };
}
function Ju(n) {
  let e, t;
  return e = new Or({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: {
        default: [e_]
      },
      $$scope: {
        ctx: n
      }
    }
  }), {
    c() {
      nt(e.$$.fragment);
    },
    m(l, i) {
      it(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[1] & /*$$scope*/
      1073741824 && (o.$$scope = {
        dirty: i,
        ctx: l
      }), e.$set(o);
    },
    i(l) {
      t || (q(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Y(e.$$.fragment, l), t = !1;
    },
    d(l) {
      lt(e, l);
    }
  };
}
function go(n) {
  var S;
  let e, t, l, i, o, s, f, r, a, c, u, d, h, p, y, L, E = (
    /*show_download_button*/
    n[13] && bo(n)
  );
  i = new au({
    props: {
      i18n: (
        /*i18n*/
        n[14]
      ),
      absolute: !1
    }
  }), i.$on(
    "clear",
    /*clear_handler*/
    n[39]
  );
  let g = (
    /*selected_image*/
    ((S = n[23]) == null ? void 0 : S.caption) && po(n)
  ), v = Pn(
    /*resolved_value*/
    n[18]
  ), b = [];
  for (let w = 0; w < v.length; w += 1)
    b[w] = wo(mo(n, v, w));
  return {
    c() {
      e = se("button"), t = se("div"), E && E.c(), l = Ze(), nt(i.$$.fragment), o = Ze(), s = se("button"), f = se("img"), u = Ze(), g && g.c(), d = Ze(), h = se("div");
      for (let w = 0; w < b.length; w += 1)
        b[w].c();
      M(t, "class", "icon-buttons svelte-yk2d08"), M(f, "data-testid", "detailed-image"), Un(f.src, r = /*selected_image*/
      n[23].image.url) || M(f, "src", r), M(f, "alt", a = /*selected_image*/
      n[23].caption || ""), M(f, "title", c = /*selected_image*/
      n[23].caption || null), M(f, "loading", "lazy"), M(f, "class", "svelte-yk2d08"), ye(f, "with-caption", !!/*selected_image*/
      n[23].caption), M(s, "class", "image-button svelte-yk2d08"), ut(s, "height", "calc(100% - " + /*selected_image*/
      (n[23].caption ? "80px" : "60px") + ")"), M(s, "aria-label", "detailed view of selected image"), M(h, "class", "thumbnails scroll-hide svelte-yk2d08"), M(h, "data-testid", "container_el"), M(e, "class", "preview svelte-yk2d08");
    },
    m(w, I) {
      ze(w, e, I), te(e, t), E && E.m(t, null), te(t, l), it(i, t, null), te(e, o), te(e, s), te(s, f), te(e, u), g && g.m(e, null), te(e, d), te(e, h);
      for (let A = 0; A < b.length; A += 1)
        b[A] && b[A].m(h, null);
      n[43](h), p = !0, y || (L = [Fn(
        s,
        "click",
        /*click_handler_1*/
        n[40]
      ), Fn(
        e,
        "keydown",
        /*on_keydown*/
        n[26]
      )], y = !0);
    },
    p(w, I) {
      var Z;
      /*show_download_button*/
      w[13] ? E ? (E.p(w, I), I[0] & /*show_download_button*/
      8192 && q(E, 1)) : (E = bo(w), E.c(), q(E, 1), E.m(t, l)) : E && (bt(), Y(E, 1, 1, () => {
        E = null;
      }), gt());
      const A = {};
      if (I[0] & /*i18n*/
      16384 && (A.i18n = /*i18n*/
      w[14]), i.$set(A), (!p || I[0] & /*selected_image*/
      8388608 && !Un(f.src, r = /*selected_image*/
      w[23].image.url)) && M(f, "src", r), (!p || I[0] & /*selected_image*/
      8388608 && a !== (a = /*selected_image*/
      w[23].caption || "")) && M(f, "alt", a), (!p || I[0] & /*selected_image*/
      8388608 && c !== (c = /*selected_image*/
      w[23].caption || null)) && M(f, "title", c), (!p || I[0] & /*selected_image*/
      8388608) && ye(f, "with-caption", !!/*selected_image*/
      w[23].caption), (!p || I[0] & /*selected_image*/
      8388608) && ut(s, "height", "calc(100% - " + /*selected_image*/
      (w[23].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (Z = w[23]) != null && Z.caption ? g ? g.p(w, I) : (g = po(w), g.c(), g.m(e, d)) : g && (g.d(1), g = null), I[0] & /*resolved_value, el, selected_index*/
      2359297) {
        v = Pn(
          /*resolved_value*/
          w[18]
        );
        let z;
        for (z = 0; z < v.length; z += 1) {
          const F = mo(w, v, z);
          b[z] ? b[z].p(F, I) : (b[z] = wo(F), b[z].c(), b[z].m(h, null));
        }
        for (; z < b.length; z += 1)
          b[z].d(1);
        b.length = v.length;
      }
    },
    i(w) {
      p || (q(E), q(i.$$.fragment, w), p = !0);
    },
    o(w) {
      Y(E), Y(i.$$.fragment, w), p = !1;
    },
    d(w) {
      w && Ue(e), E && E.d(), lt(i), g && g.d(), _a(b, w), n[43](null), y = !1, Gu(L);
    }
  };
}
function bo(n) {
  let e, t, l;
  return t = new dt({
    props: {
      show_label: !0,
      label: (
        /*i18n*/
        n[14]("common.download")
      ),
      Icon: Co
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[38]
  ), {
    c() {
      e = se("div"), nt(t.$$.fragment), M(e, "class", "download-button-container svelte-yk2d08");
    },
    m(i, o) {
      ze(i, e, o), it(t, e, null), l = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      16384 && (s.label = /*i18n*/
      i[14]("common.download")), t.$set(s);
    },
    i(i) {
      l || (q(t.$$.fragment, i), l = !0);
    },
    o(i) {
      Y(t.$$.fragment, i), l = !1;
    },
    d(i) {
      i && Ue(e), lt(t);
    }
  };
}
function po(n) {
  let e, t = (
    /*selected_image*/
    n[23].caption + ""
  ), l;
  return {
    c() {
      e = se("caption"), l = ma(t), M(e, "class", "caption svelte-yk2d08");
    },
    m(i, o) {
      ze(i, e, o), te(e, l);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      8388608 && t !== (t = /*selected_image*/
      i[23].caption + "") && da(l, t);
    },
    d(i) {
      i && Ue(e);
    }
  };
}
function wo(n) {
  let e, t, l, i, o, s, f = (
    /*i*/
    n[59]
  ), r, a;
  const c = () => (
    /*button_binding*/
    n[41](e, f)
  ), u = () => (
    /*button_binding*/
    n[41](null, f)
  );
  function d() {
    return (
      /*click_handler_2*/
      n[42](
        /*i*/
        n[59]
      )
    );
  }
  return {
    c() {
      e = se("button"), t = se("img"), o = Ze(), Un(t.src, l = /*entry*/
      n[57].image.url) || M(t, "src", l), M(t, "title", i = /*entry*/
      n[57].caption || null), M(t, "data-testid", "thumbnail " + /*i*/
      (n[59] + 1)), M(t, "alt", ""), M(t, "loading", "lazy"), M(t, "class", "svelte-yk2d08"), M(e, "class", "thumbnail-item thumbnail-small svelte-yk2d08"), M(e, "aria-label", s = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length), ye(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    m(h, p) {
      ze(h, e, p), te(e, t), te(e, o), c(), r || (a = Fn(e, "click", d), r = !0);
    },
    p(h, p) {
      n = h, p[0] & /*resolved_value*/
      262144 && !Un(t.src, l = /*entry*/
      n[57].image.url) && M(t, "src", l), p[0] & /*resolved_value*/
      262144 && i !== (i = /*entry*/
      n[57].caption || null) && M(t, "title", i), p[0] & /*resolved_value*/
      262144 && s !== (s = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length) && M(e, "aria-label", s), f !== /*i*/
      n[59] && (u(), f = /*i*/
      n[59], c()), p[0] & /*selected_index*/
      1 && ye(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    d(h) {
      h && Ue(e), u(), r = !1, a();
    }
  };
}
function ko(n) {
  let e, t, l;
  return t = new Ws({
    props: {
      i18n: (
        /*i18n*/
        n[14]
      ),
      value: (
        /*resolved_value*/
        n[18]
      ),
      formatter: Lu
    }
  }), t.$on(
    "share",
    /*share_handler*/
    n[44]
  ), t.$on(
    "error",
    /*error_handler*/
    n[45]
  ), {
    c() {
      e = se("div"), nt(t.$$.fragment), M(e, "class", "icon-button svelte-yk2d08");
    },
    m(i, o) {
      ze(i, e, o), it(t, e, null), l = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      16384 && (s.i18n = /*i18n*/
      i[14]), o[0] & /*resolved_value*/
      262144 && (s.value = /*resolved_value*/
      i[18]), t.$set(s);
    },
    i(i) {
      l || (q(t.$$.fragment, i), l = !0);
    },
    o(i) {
      Y(t.$$.fragment, i), l = !1;
    },
    d(i) {
      i && Ue(e), lt(t);
    }
  };
}
function vo(n) {
  let e, t, l, i, o;
  function s() {
    return (
      /*click_handler_3*/
      n[46](
        /*i*/
        n[59]
      )
    );
  }
  function f() {
    return (
      /*label_click_handler*/
      n[47](
        /*i*/
        n[59],
        /*entry*/
        n[57]
      )
    );
  }
  function r(...a) {
    return (
      /*like_handler*/
      n[48](
        /*i*/
        n[59],
        /*entry*/
        n[57],
        ...a
      )
    );
  }
  return t = new Su({
    props: {
      likeable: (
        /*likeable*/
        n[11]
      ),
      clickable: (
        /*clickable*/
        n[12]
      ),
      value: (
        /*entry*/
        n[57]
      ),
      action_label: (
        /*action_label*/
        n[6]
      )
    }
  }), t.$on("click", s), t.$on("label_click", f), t.$on("like", r), {
    c() {
      e = se("div"), nt(t.$$.fragment), l = Ze(), M(e, "class", "thumbnail-item thumbnail-lg svelte-yk2d08"), M(e, "aria-label", i = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length), ye(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    m(a, c) {
      ze(a, e, c), it(t, e, null), te(e, l), o = !0;
    },
    p(a, c) {
      n = a;
      const u = {};
      c[0] & /*likeable*/
      2048 && (u.likeable = /*likeable*/
      n[11]), c[0] & /*clickable*/
      4096 && (u.clickable = /*clickable*/
      n[12]), c[0] & /*resolved_value*/
      262144 && (u.value = /*entry*/
      n[57]), c[0] & /*action_label*/
      64 && (u.action_label = /*action_label*/
      n[6]), t.$set(u), (!o || c[0] & /*resolved_value*/
      262144 && i !== (i = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length)) && M(e, "aria-label", i), (!o || c[0] & /*selected_index*/
      1) && ye(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    i(a) {
      o || (q(t.$$.fragment, a), o = !0);
    },
    o(a) {
      Y(t.$$.fragment, a), o = !1;
    },
    d(a) {
      a && Ue(e), lt(t);
    }
  };
}
function Qu(n) {
  let e, t;
  const l = [
    /*load_more_button_props*/
    n[15]
  ];
  let i = {
    $$slots: {
      default: [$u]
    },
    $$scope: {
      ctx: n
    }
  };
  for (let o = 0; o < l.length; o += 1)
    i = Fu(i, l[o]);
  return e = new Ac({
    props: i
  }), e.$on(
    "click",
    /*click_handler_4*/
    n[50]
  ), {
    c() {
      nt(e.$$.fragment);
    },
    m(o, s) {
      it(e, o, s), t = !0;
    },
    p(o, s) {
      const f = s[0] & /*load_more_button_props*/
      32768 ? Hu(l, [qu(
        /*load_more_button_props*/
        o[15]
      )]) : {};
      s[0] & /*i18n, load_more_button_props*/
      49152 | s[1] & /*$$scope*/
      1073741824 && (f.$$scope = {
        dirty: s,
        ctx: o
      }), e.$set(f);
    },
    i(o) {
      t || (q(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Y(e.$$.fragment, o), t = !1;
    },
    d(o) {
      lt(e, o);
    }
  };
}
function xu(n) {
  let e, t;
  return e = new Oo({
    props: {
      margin: !1
    }
  }), {
    c() {
      nt(e.$$.fragment);
    },
    m(l, i) {
      it(e, l, i), t = !0;
    },
    p: Wu,
    i(l) {
      t || (q(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Y(e.$$.fragment, l), t = !1;
    },
    d(l) {
      lt(e, l);
    }
  };
}
function $u(n) {
  let e = (
    /*i18n*/
    n[14](
      /*load_more_button_props*/
      n[15].value || /*load_more_button_props*/
      n[15].label || "Load More"
    ) + ""
  ), t;
  return {
    c() {
      t = ma(e);
    },
    m(l, i) {
      ze(l, t, i);
    },
    p(l, i) {
      i[0] & /*i18n, load_more_button_props*/
      49152 && e !== (e = /*i18n*/
      l[14](
        /*load_more_button_props*/
        l[15].value || /*load_more_button_props*/
        l[15].label || "Load More"
      ) + "") && da(t, e);
    },
    d(l) {
      l && Ue(t);
    }
  };
}
function e_(n) {
  let e, t;
  return e = new Lo({}), {
    c() {
      nt(e.$$.fragment);
    },
    m(l, i) {
      it(e, l, i), t = !0;
    },
    i(l) {
      t || (q(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Y(e.$$.fragment, l), t = !1;
    },
    d(l) {
      lt(e, l);
    }
  };
}
function t_(n) {
  let e, t, l, i, o, s, f;
  ua(
    /*onwindowresize*/
    n[37]
  );
  let r = (
    /*show_label*/
    n[2] && ho(n)
  );
  const a = [Ju, Ku], c = [];
  function u(d, h) {
    return !/*value*/
    d[7] || !/*resolved_value*/
    d[18] || /*resolved_value*/
    d[18].length === 0 ? 0 : 1;
  }
  return t = u(n), l = c[t] = a[t](n), {
    c() {
      r && r.c(), e = Ze(), l.c(), i = zu();
    },
    m(d, h) {
      r && r.m(d, h), ze(d, e, h), c[t].m(d, h), ze(d, i, h), o = !0, s || (f = Fn(
        Ml,
        "resize",
        /*onwindowresize*/
        n[37]
      ), s = !0);
    },
    p(d, h) {
      /*show_label*/
      d[2] ? r ? (r.p(d, h), h[0] & /*show_label*/
      4 && q(r, 1)) : (r = ho(d), r.c(), q(r, 1), r.m(e.parentNode, e)) : r && (bt(), Y(r, 1, 1, () => {
        r = null;
      }), gt());
      let p = t;
      t = u(d), t === p ? c[t].p(d, h) : (bt(), Y(c[p], 1, 1, () => {
        c[p] = null;
      }), gt(), l = c[t], l ? l.p(d, h) : (l = c[t] = a[t](d), l.c()), q(l, 1), l.m(i.parentNode, i));
    },
    i(d) {
      o || (q(r), q(l), o = !0);
    },
    o(d) {
      Y(r), Y(l), o = !1;
    },
    d(d) {
      d && (Ue(e), Ue(i)), r && r.d(d), c[t].d(d), s = !1, f();
    }
  };
}
async function n_(n, e) {
  let t;
  try {
    t = await fetch(n);
  } catch (s) {
    if (s instanceof TypeError) {
      window.open(n, "_blank", "noreferrer");
      return;
    }
    throw s;
  }
  const l = await t.blob(), i = URL.createObjectURL(l), o = document.createElement("a");
  o.href = i, o.download = e, o.click(), URL.revokeObjectURL(i);
}
function l_(n, e, t) {
  let l, i, o, {
    object_fit: s = "cover"
  } = e, {
    show_label: f = !0
  } = e, {
    has_more: r = !1
  } = e, {
    label: a
  } = e, {
    pending: c
  } = e, {
    action_label: u
  } = e, {
    value: d = null
  } = e, {
    columns: h = [2]
  } = e, {
    height: p = "auto"
  } = e, {
    preview: y
  } = e, {
    root: L
  } = e, {
    proxy_url: E
  } = e, {
    allow_preview: g = !0
  } = e, {
    show_share_button: v = !1
  } = e, {
    likeable: b
  } = e, {
    clickable: S
  } = e, {
    show_download_button: w = !1
  } = e, {
    i18n: I
  } = e, {
    selected_index: A = null
  } = e, {
    gap: Z = 8
  } = e, {
    load_more_button_props: z = {}
  } = e, F, H = [], ce, J = 0, ke = 0, x = 0;
  const be = Yu();
  let ve = !0, ie = null, G = null, U = d;
  A == null && y && (d != null && d.length) && (A = 0);
  let qe = A;
  function W(k) {
    const B = k.target, $ = k.clientX, Tt = B.offsetWidth / 2;
    $ < Tt ? t(0, A = l) : t(0, A = i);
  }
  function ot(k) {
    switch (k.code) {
      case "Escape":
        k.preventDefault(), t(0, A = null);
        break;
      case "ArrowLeft":
        k.preventDefault(), t(0, A = l);
        break;
      case "ArrowRight":
        k.preventDefault(), t(0, A = i);
        break;
    }
  }
  const m = [];
  let ue;
  async function Ft(k) {
    var Wt;
    if (typeof k != "number" || (await Zu(), m[k] === void 0)) return;
    (Wt = m[k]) == null || Wt.focus();
    const {
      left: B,
      width: $
    } = ue.getBoundingClientRect(), {
      left: jt,
      width: Tt
    } = m[k].getBoundingClientRect(), yt = jt - B + Tt / 2 - $ / 2 + ue.scrollLeft;
    ue && typeof ue.scrollTo == "function" && ue.scrollTo({
      left: yt < 0 ? 0 : yt,
      behavior: "smooth"
    });
  }
  function sn() {
    ie == null || ie.unmount(), ie = new Nu(F, {
      cols: ce,
      gap: Z
    });
  }
  Xu(() => {
    ie == null || ie.unmount();
  });
  function Ut() {
    t(20, ke = Ml.innerHeight), t(17, x = Ml.innerWidth);
  }
  const fn = () => {
    const k = o == null ? void 0 : o.image;
    if (!k)
      return;
    const {
      url: B,
      orig_name: $
    } = k;
    B && n_(B, $ ?? "image");
  }, cn = () => t(0, A = null), at = (k) => W(k);
  function zt(k, B) {
    vl[k ? "unshift" : "push"](() => {
      m[B] = k, t(21, m);
    });
  }
  const Ke = (k) => t(0, A = k);
  function qt(k) {
    vl[k ? "unshift" : "push"](() => {
      ue = k, t(22, ue);
    });
  }
  const Ht = (k) => {
    Cu(k.detail.description);
  };
  function rt(k) {
    Uu.call(this, n, k);
  }
  const vt = (k) => t(0, A = k), Et = (k, B) => {
    be("click", {
      index: k,
      value: B
    });
  }, un = (k, B, $) => {
    be("like", {
      index: k,
      value: B,
      liked: $.detail
    });
  };
  function _n(k) {
    vl[k ? "unshift" : "push"](() => {
      F = k, t(16, F);
    });
  }
  const Wn = () => {
    be("load_more");
  };
  function Bt() {
    J = this.clientHeight, t(19, J);
  }
  return n.$$set = (k) => {
    "object_fit" in k && t(1, s = k.object_fit), "show_label" in k && t(2, f = k.show_label), "has_more" in k && t(3, r = k.has_more), "label" in k && t(4, a = k.label), "pending" in k && t(5, c = k.pending), "action_label" in k && t(6, u = k.action_label), "value" in k && t(7, d = k.value), "columns" in k && t(27, h = k.columns), "height" in k && t(8, p = k.height), "preview" in k && t(28, y = k.preview), "root" in k && t(29, L = k.root), "proxy_url" in k && t(30, E = k.proxy_url), "allow_preview" in k && t(9, g = k.allow_preview), "show_share_button" in k && t(10, v = k.show_share_button), "likeable" in k && t(11, b = k.likeable), "clickable" in k && t(12, S = k.clickable), "show_download_button" in k && t(13, w = k.show_download_button), "i18n" in k && t(14, I = k.i18n), "selected_index" in k && t(0, A = k.selected_index), "gap" in k && t(31, Z = k.gap), "load_more_button_props" in k && t(15, z = k.load_more_button_props);
  }, n.$$.update = () => {
    if (n.$$.dirty[0] & /*columns*/
    134217728)
      if (typeof h == "object" && h !== null)
        if (Array.isArray(h)) {
          const k = h.length;
          t(32, H = kl.map((B, $) => [B.width, h[$] ?? h[k - 1]]));
        } else {
          let k = 0;
          t(32, H = kl.map((B) => (k = h[B.key] ?? k, [B.width, k])));
        }
      else
        t(32, H = kl.map((k) => [k.width, h]));
    if (n.$$.dirty[0] & /*window_width*/
    131072 | n.$$.dirty[1] & /*breakpointColumns*/
    2) {
      for (const [k, B] of [...H].reverse())
        if (x >= k) {
          t(33, ce = B);
          break;
        }
    }
    n.$$.dirty[0] & /*value*/
    128 | n.$$.dirty[1] & /*was_reset*/
    8 && t(34, ve = d == null || d.length === 0 ? !0 : ve), n.$$.dirty[0] & /*value, root, proxy_url*/
    1610612864 && t(18, G = d == null ? null : d.map((k) => (k.image = ra(k.image, L, E), k))), n.$$.dirty[0] & /*value, preview, selected_index*/
    268435585 | n.$$.dirty[1] & /*prev_value, was_reset*/
    24 && ($t(U, d) || (ve ? (t(0, A = y && (d != null && d.length) ? 0 : null), t(34, ve = !1), ie = null) : t(0, A = A != null && d != null && A < d.length ? A : null), be("change"), t(35, U = d))), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (l = ((A ?? 0) + ((G == null ? void 0 : G.length) ?? 0) - 1) % ((G == null ? void 0 : G.length) ?? 0)), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (i = ((A ?? 0) + 1) % ((G == null ? void 0 : G.length) ?? 0)), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 | n.$$.dirty[1] & /*old_selected_index*/
    32 && A !== qe && (t(36, qe = A), A !== null && be("select", {
      index: A,
      value: G == null ? void 0 : G[A]
    })), n.$$.dirty[0] & /*allow_preview, selected_index*/
    513 && g && Ft(A), n.$$.dirty[0] & /*waterfall_grid_el*/
    65536 | n.$$.dirty[1] & /*cols*/
    4 && F && sn(), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && t(23, o = A != null && G != null ? G[A] : null);
  }, [A, s, f, r, a, c, u, d, p, g, v, b, S, w, I, z, F, x, G, J, ke, m, ue, o, be, W, ot, h, y, L, E, Z, H, ce, ve, U, qe, Ut, fn, cn, at, zt, Ke, qt, Ht, rt, vt, Et, un, _n, Wn, Bt];
}
class i_ extends Mu {
  constructor(e) {
    super(), ju(this, e, l_, t_, Vu, {
      object_fit: 1,
      show_label: 2,
      has_more: 3,
      label: 4,
      pending: 5,
      action_label: 6,
      value: 7,
      columns: 27,
      height: 8,
      preview: 28,
      root: 29,
      proxy_url: 30,
      allow_preview: 9,
      show_share_button: 10,
      likeable: 11,
      clickable: 12,
      show_download_button: 13,
      i18n: 14,
      selected_index: 0,
      gap: 31,
      load_more_button_props: 15
    }, null, [-1, -1]);
  }
}
const {
  SvelteComponent: o_,
  add_flush_callback: a_,
  assign: r_,
  bind: s_,
  binding_callbacks: f_,
  check_outros: c_,
  create_component: ql,
  destroy_component: Hl,
  detach: u_,
  get_spread_object: __,
  get_spread_update: d_,
  group_outros: m_,
  init: h_,
  insert: g_,
  mount_component: Bl,
  safe_not_equal: b_,
  space: p_,
  transition_in: Nt,
  transition_out: tn
} = window.__gradio__svelte__internal, {
  createEventDispatcher: w_
} = window.__gradio__svelte__internal;
function Eo(n) {
  let e, t;
  const l = [
    {
      autoscroll: (
        /*gradio*/
        n[25].autoscroll
      )
    },
    {
      i18n: (
        /*gradio*/
        n[25].i18n
      )
    },
    /*loading_status*/
    n[1],
    {
      show_progress: (
        /*loading_status*/
        n[1].show_progress === "hidden" ? "hidden" : (
          /*has_more*/
          n[3] ? "minimal" : (
            /*loading_status*/
            n[1].show_progress
          )
        )
      )
    }
  ];
  let i = {};
  for (let o = 0; o < l.length; o += 1)
    i = r_(i, l[o]);
  return e = new Xf({
    props: i
  }), {
    c() {
      ql(e.$$.fragment);
    },
    m(o, s) {
      Bl(e, o, s), t = !0;
    },
    p(o, s) {
      const f = s[0] & /*gradio, loading_status, has_more*/
      33554442 ? d_(l, [s[0] & /*gradio*/
      33554432 && {
        autoscroll: (
          /*gradio*/
          o[25].autoscroll
        )
      }, s[0] & /*gradio*/
      33554432 && {
        i18n: (
          /*gradio*/
          o[25].i18n
        )
      }, s[0] & /*loading_status*/
      2 && __(
        /*loading_status*/
        o[1]
      ), s[0] & /*loading_status, has_more*/
      10 && {
        show_progress: (
          /*loading_status*/
          o[1].show_progress === "hidden" ? "hidden" : (
            /*has_more*/
            o[3] ? "minimal" : (
              /*loading_status*/
              o[1].show_progress
            )
          )
        )
      }]) : {};
      e.$set(f);
    },
    i(o) {
      t || (Nt(e.$$.fragment, o), t = !0);
    },
    o(o) {
      tn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      Hl(e, o);
    }
  };
}
function k_(n) {
  var r;
  let e, t, l, i, o = (
    /*loading_status*/
    n[1] && Eo(n)
  );
  function s(a) {
    n[29](a);
  }
  let f = {
    pending: (
      /*loading_status*/
      ((r = n[1]) == null ? void 0 : r.status) === "pending"
    ),
    likeable: (
      /*likeable*/
      n[10]
    ),
    clickable: (
      /*clickable*/
      n[11]
    ),
    label: (
      /*label*/
      n[4]
    ),
    action_label: (
      /*action_label*/
      n[5]
    ),
    value: (
      /*value*/
      n[9]
    ),
    root: (
      /*root*/
      n[23]
    ),
    proxy_url: (
      /*proxy_url*/
      n[24]
    ),
    show_label: (
      /*show_label*/
      n[2]
    ),
    object_fit: (
      /*object_fit*/
      n[21]
    ),
    load_more_button_props: (
      /*_load_more_button_props*/
      n[26]
    ),
    has_more: (
      /*has_more*/
      n[3]
    ),
    columns: (
      /*columns*/
      n[15]
    ),
    height: (
      /*height*/
      n[17]
    ),
    preview: (
      /*preview*/
      n[18]
    ),
    gap: (
      /*gap*/
      n[16]
    ),
    allow_preview: (
      /*allow_preview*/
      n[19]
    ),
    show_share_button: (
      /*show_share_button*/
      n[20]
    ),
    show_download_button: (
      /*show_download_button*/
      n[22]
    ),
    i18n: (
      /*gradio*/
      n[25].i18n
    )
  };
  return (
    /*selected_index*/
    n[0] !== void 0 && (f.selected_index = /*selected_index*/
    n[0]), t = new i_({
      props: f
    }), f_.push(() => s_(t, "selected_index", s)), t.$on(
      "click",
      /*click_handler*/
      n[30]
    ), t.$on(
      "change",
      /*change_handler*/
      n[31]
    ), t.$on(
      "like",
      /*like_handler*/
      n[32]
    ), t.$on(
      "select",
      /*select_handler*/
      n[33]
    ), t.$on(
      "share",
      /*share_handler*/
      n[34]
    ), t.$on(
      "error",
      /*error_handler*/
      n[35]
    ), t.$on(
      "load_more",
      /*load_more_handler*/
      n[36]
    ), {
      c() {
        o && o.c(), e = p_(), ql(t.$$.fragment);
      },
      m(a, c) {
        o && o.m(a, c), g_(a, e, c), Bl(t, a, c), i = !0;
      },
      p(a, c) {
        var d;
        /*loading_status*/
        a[1] ? o ? (o.p(a, c), c[0] & /*loading_status*/
        2 && Nt(o, 1)) : (o = Eo(a), o.c(), Nt(o, 1), o.m(e.parentNode, e)) : o && (m_(), tn(o, 1, 1, () => {
          o = null;
        }), c_());
        const u = {};
        c[0] & /*loading_status*/
        2 && (u.pending = /*loading_status*/
        ((d = a[1]) == null ? void 0 : d.status) === "pending"), c[0] & /*likeable*/
        1024 && (u.likeable = /*likeable*/
        a[10]), c[0] & /*clickable*/
        2048 && (u.clickable = /*clickable*/
        a[11]), c[0] & /*label*/
        16 && (u.label = /*label*/
        a[4]), c[0] & /*action_label*/
        32 && (u.action_label = /*action_label*/
        a[5]), c[0] & /*value*/
        512 && (u.value = /*value*/
        a[9]), c[0] & /*root*/
        8388608 && (u.root = /*root*/
        a[23]), c[0] & /*proxy_url*/
        16777216 && (u.proxy_url = /*proxy_url*/
        a[24]), c[0] & /*show_label*/
        4 && (u.show_label = /*show_label*/
        a[2]), c[0] & /*object_fit*/
        2097152 && (u.object_fit = /*object_fit*/
        a[21]), c[0] & /*_load_more_button_props*/
        67108864 && (u.load_more_button_props = /*_load_more_button_props*/
        a[26]), c[0] & /*has_more*/
        8 && (u.has_more = /*has_more*/
        a[3]), c[0] & /*columns*/
        32768 && (u.columns = /*columns*/
        a[15]), c[0] & /*height*/
        131072 && (u.height = /*height*/
        a[17]), c[0] & /*preview*/
        262144 && (u.preview = /*preview*/
        a[18]), c[0] & /*gap*/
        65536 && (u.gap = /*gap*/
        a[16]), c[0] & /*allow_preview*/
        524288 && (u.allow_preview = /*allow_preview*/
        a[19]), c[0] & /*show_share_button*/
        1048576 && (u.show_share_button = /*show_share_button*/
        a[20]), c[0] & /*show_download_button*/
        4194304 && (u.show_download_button = /*show_download_button*/
        a[22]), c[0] & /*gradio*/
        33554432 && (u.i18n = /*gradio*/
        a[25].i18n), !l && c[0] & /*selected_index*/
        1 && (l = !0, u.selected_index = /*selected_index*/
        a[0], a_(() => l = !1)), t.$set(u);
      },
      i(a) {
        i || (Nt(o), Nt(t.$$.fragment, a), i = !0);
      },
      o(a) {
        tn(o), tn(t.$$.fragment, a), i = !1;
      },
      d(a) {
        a && u_(e), o && o.d(a), Hl(t, a);
      }
    }
  );
}
function v_(n) {
  let e, t;
  return e = new qa({
    props: {
      visible: (
        /*visible*/
        n[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[6]
      ),
      elem_classes: (
        /*elem_classes*/
        n[7]
      ),
      container: (
        /*container*/
        n[12]
      ),
      scale: (
        /*scale*/
        n[13]
      ),
      min_width: (
        /*min_width*/
        n[14]
      ),
      allow_overflow: !1,
      $$slots: {
        default: [k_]
      },
      $$scope: {
        ctx: n
      }
    }
  }), {
    c() {
      ql(e.$$.fragment);
    },
    m(l, i) {
      Bl(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      l[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      l[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      l[7]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      l[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      l[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      l[14]), i[0] & /*loading_status, likeable, clickable, label, action_label, value, root, proxy_url, show_label, object_fit, _load_more_button_props, has_more, columns, height, preview, gap, allow_preview, show_share_button, show_download_button, gradio, selected_index*/
      134188607 | i[1] & /*$$scope*/
      128 && (o.$$scope = {
        dirty: i,
        ctx: l
      }), e.$set(o);
    },
    i(l) {
      t || (Nt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      tn(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Hl(e, l);
    }
  };
}
function E_(n, e, t) {
  let {
    loading_status: l
  } = e, {
    show_label: i
  } = e, {
    has_more: o
  } = e, {
    label: s
  } = e, {
    action_label: f
  } = e, {
    elem_id: r = ""
  } = e, {
    elem_classes: a = []
  } = e, {
    visible: c = !0
  } = e, {
    value: u = null
  } = e, {
    likeable: d
  } = e, {
    clickable: h
  } = e, {
    container: p = !0
  } = e, {
    scale: y = null
  } = e, {
    min_width: L = void 0
  } = e, {
    columns: E = [2]
  } = e, {
    gap: g = 8
  } = e, {
    height: v = "auto"
  } = e, {
    preview: b
  } = e, {
    allow_preview: S = !0
  } = e, {
    selected_index: w = null
  } = e, {
    show_share_button: I = !1
  } = e, {
    object_fit: A = "cover"
  } = e, {
    show_download_button: Z = !1
  } = e, {
    root: z
  } = e, {
    proxy_url: F
  } = e, {
    gradio: H
  } = e, {
    load_more_button_props: ce = {}
  } = e, J = {};
  const ke = w_(), x = (m) => {
    H.dispatch("like", m);
  };
  function be(m) {
    w = m, t(0, w);
  }
  const ve = (m) => H.dispatch("click", m.detail), ie = () => H.dispatch("change", u), G = (m) => x(m.detail), U = (m) => H.dispatch("select", m.detail), qe = (m) => H.dispatch("share", m.detail), W = (m) => H.dispatch("error", m.detail), ot = () => {
    H.dispatch("load_more", u);
  };
  return n.$$set = (m) => {
    "loading_status" in m && t(1, l = m.loading_status), "show_label" in m && t(2, i = m.show_label), "has_more" in m && t(3, o = m.has_more), "label" in m && t(4, s = m.label), "action_label" in m && t(5, f = m.action_label), "elem_id" in m && t(6, r = m.elem_id), "elem_classes" in m && t(7, a = m.elem_classes), "visible" in m && t(8, c = m.visible), "value" in m && t(9, u = m.value), "likeable" in m && t(10, d = m.likeable), "clickable" in m && t(11, h = m.clickable), "container" in m && t(12, p = m.container), "scale" in m && t(13, y = m.scale), "min_width" in m && t(14, L = m.min_width), "columns" in m && t(15, E = m.columns), "gap" in m && t(16, g = m.gap), "height" in m && t(17, v = m.height), "preview" in m && t(18, b = m.preview), "allow_preview" in m && t(19, S = m.allow_preview), "selected_index" in m && t(0, w = m.selected_index), "show_share_button" in m && t(20, I = m.show_share_button), "object_fit" in m && t(21, A = m.object_fit), "show_download_button" in m && t(22, Z = m.show_download_button), "root" in m && t(23, z = m.root), "proxy_url" in m && t(24, F = m.proxy_url), "gradio" in m && t(25, H = m.gradio), "load_more_button_props" in m && t(28, ce = m.load_more_button_props);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*_load_more_button_props, load_more_button_props*/
    335544320 && t(26, J = {
      ...J,
      ...ce
    }), n.$$.dirty[0] & /*selected_index*/
    1 && ke("prop_change", {
      selected_index: w
    });
  }, [w, l, i, o, s, f, r, a, c, u, d, h, p, y, L, E, g, v, b, S, I, A, Z, z, F, H, J, x, ce, be, ve, ie, G, U, qe, W, ot];
}
class R_ extends o_ {
  constructor(e) {
    super(), h_(this, e, E_, v_, b_, {
      loading_status: 1,
      show_label: 2,
      has_more: 3,
      label: 4,
      action_label: 5,
      elem_id: 6,
      elem_classes: 7,
      visible: 8,
      value: 9,
      likeable: 10,
      clickable: 11,
      container: 12,
      scale: 13,
      min_width: 14,
      columns: 15,
      gap: 16,
      height: 17,
      preview: 18,
      allow_preview: 19,
      selected_index: 0,
      show_share_button: 20,
      object_fit: 21,
      show_download_button: 22,
      root: 23,
      proxy_url: 24,
      gradio: 25,
      load_more_button_props: 28
    }, null, [-1, -1]);
  }
}
export {
  i_ as BaseGallery,
  R_ as default
};
