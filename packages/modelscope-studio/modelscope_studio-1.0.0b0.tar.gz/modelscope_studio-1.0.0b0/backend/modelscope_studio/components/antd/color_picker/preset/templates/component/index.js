function X(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((s, o) => {
    const l = o.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
        const b = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        s[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const h = {
            ...n.props[c[a]] || {}
          };
          m[c[a]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, s;
      }
      const _ = c[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return s;
  }, {});
}
function j() {
}
function Y(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function D(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return j;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return D(e, (i) => t = i)(), t;
}
const p = [];
function y(e, t = j) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function s(u) {
    if (Y(e, u) && (e = u, i)) {
      const c = !p.length;
      for (const f of n)
        f[1](), p.push(f, e);
      if (c) {
        for (let f = 0; f < p.length; f += 2)
          p[f][0](p[f + 1]);
        p.length = 0;
      }
    }
  }
  function o(u) {
    s(u(e));
  }
  function l(u, c = j) {
    const f = [u, c];
    return n.add(f), n.size === 1 && (i = t(s, o) || j), u(e), () => {
      n.delete(f), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: s,
    update: o,
    subscribe: l
  };
}
const {
  getContext: F,
  setContext: P
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function Z() {
  const e = y({});
  return P(L, e);
}
const B = "$$ms-gr-antd-context-key";
function G(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = V(), i = Q({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    i.slotKey.set(c);
  }), H();
  const n = F(B), s = ((u = g(n)) == null ? void 0 : u.as_item) || e.as_item, o = n ? s ? g(n)[s] : g(n) : {}, l = y({
    ...e,
    ...o
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: f
    } = g(l);
    f && (c = c[f]), l.update((_) => ({
      ..._,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? g(n)[c.as_item] : g(n);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function H() {
  P(M, y(void 0));
}
function V() {
  return F(M);
}
const J = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: e,
  index: t,
  subIndex: i
}) {
  return P(J, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function T(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var z = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var o = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (o = s(o, n(u)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return i.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var l = "";
      for (var u in o)
        t.call(o, u) && o[u] && (l = s(l, u));
      return l;
    }
    function s(o, l) {
      return l ? o ? o + " " + l : o + l : o;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(z);
var W = z.exports;
const $ = /* @__PURE__ */ T(W), {
  getContext: tt,
  setContext: et
} = window.__gradio__svelte__internal;
function nt(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(s = ["default"]) {
    const o = s.reduce((l, u) => (l[u] = y([]), l), {});
    return et(t, {
      itemsMap: o,
      allowedSlots: s
    }), o;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: o
    } = tt(t);
    return function(l, u, c) {
      s && (l ? s[l].update((f) => {
        const _ = [...f];
        return o.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : o.includes("default") && s.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: gt,
  getSetItemFn: st
} = nt("color-picker"), {
  SvelteComponent: it,
  check_outros: ot,
  component_subscribe: k,
  create_slot: lt,
  detach: rt,
  empty: ct,
  flush: d,
  get_all_dirty_from_scope: ut,
  get_slot_changes: ft,
  group_outros: at,
  init: _t,
  insert: mt,
  safe_not_equal: dt,
  transition_in: v,
  transition_out: O,
  update_slot_base: bt
} = window.__gradio__svelte__internal;
function A(e) {
  let t;
  const i = (
    /*#slots*/
    e[20].default
  ), n = lt(
    i,
    e,
    /*$$scope*/
    e[19],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, o) {
      n && n.m(s, o), t = !0;
    },
    p(s, o) {
      n && n.p && (!t || o & /*$$scope*/
      524288) && bt(
        n,
        i,
        s,
        /*$$scope*/
        s[19],
        t ? ft(
          i,
          /*$$scope*/
          s[19],
          o,
          null
        ) : ut(
          /*$$scope*/
          s[19]
        ),
        null
      );
    },
    i(s) {
      t || (v(n, s), t = !0);
    },
    o(s) {
      O(n, s), t = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function yt(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && A(e)
  );
  return {
    c() {
      n && n.c(), t = ct();
    },
    m(s, o) {
      n && n.m(s, o), mt(s, t, o), i = !0;
    },
    p(s, [o]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, o), o & /*$mergedProps*/
      1 && v(n, 1)) : (n = A(s), n.c(), v(n, 1), n.m(t.parentNode, t)) : n && (at(), O(n, 1, 1, () => {
        n = null;
      }), ot());
    },
    i(s) {
      i || (v(n), i = !0);
    },
    o(s) {
      O(n), i = !1;
    },
    d(s) {
      s && rt(t), n && n.d(s);
    }
  };
}
function ht(e, t, i) {
  let n, s, o, l, {
    $$slots: u = {},
    $$scope: c
  } = t, {
    gradio: f
  } = t, {
    props: _ = {}
  } = t;
  const m = y(_);
  k(e, m, (r) => i(18, l = r));
  let {
    _internal: b = {}
  } = t, {
    colors: a
  } = t, {
    label: h
  } = t, {
    default_open: x
  } = t, {
    as_item: C
  } = t, {
    visible: K = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: I = {}
  } = t;
  const E = V();
  k(e, E, (r) => i(17, o = r));
  const [N, R] = G({
    gradio: f,
    props: l,
    _internal: b,
    visible: K,
    elem_id: S,
    elem_classes: w,
    elem_style: I,
    as_item: C,
    colors: a,
    default_open: x,
    label: h
  });
  k(e, N, (r) => i(0, s = r));
  const q = Z();
  k(e, q, (r) => i(16, n = r));
  const U = st();
  return e.$$set = (r) => {
    "gradio" in r && i(5, f = r.gradio), "props" in r && i(6, _ = r.props), "_internal" in r && i(7, b = r._internal), "colors" in r && i(8, a = r.colors), "label" in r && i(9, h = r.label), "default_open" in r && i(10, x = r.default_open), "as_item" in r && i(11, C = r.as_item), "visible" in r && i(12, K = r.visible), "elem_id" in r && i(13, S = r.elem_id), "elem_classes" in r && i(14, w = r.elem_classes), "elem_style" in r && i(15, I = r.elem_style), "$$scope" in r && i(19, c = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    64 && m.update((r) => ({
      ...r,
      ..._
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, colors, default_open, label*/
    327584 && R({
      gradio: f,
      props: l,
      _internal: b,
      visible: K,
      elem_id: S,
      elem_classes: w,
      elem_style: I,
      as_item: C,
      colors: a,
      default_open: x,
      label: h
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    196609 && U(o, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: $(s.elem_classes, "ms-gr-antd-color-picker-preset"),
        id: s.elem_id,
        label: s.label,
        colors: s.colors,
        defaultOpen: s.default_open,
        ...s.props,
        ...X(s)
      },
      slots: n
    });
  }, [s, m, E, N, q, f, _, b, a, h, x, C, K, S, w, I, n, o, l, c, u];
}
class pt extends it {
  constructor(t) {
    super(), _t(this, t, ht, yt, dt, {
      gradio: 5,
      props: 6,
      _internal: 7,
      colors: 8,
      label: 9,
      default_open: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get colors() {
    return this.$$.ctx[8];
  }
  set colors(t) {
    this.$$set({
      colors: t
    }), d();
  }
  get label() {
    return this.$$.ctx[9];
  }
  set label(t) {
    this.$$set({
      label: t
    }), d();
  }
  get default_open() {
    return this.$$.ctx[10];
  }
  set default_open(t) {
    this.$$set({
      default_open: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  pt as default
};
